import pickle
import socket

from constants import NetworkEvents


class ServerNetwork:
    def __init__(self, should_connect, on_connect, on_disconnect):
        self.server_ip = "127.0.0.1"
        self.server_port = 5555
        self.clients = set()
        self.should_connect = should_connect
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect

    def create_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.server_ip, self.server_port))

    def wait_for_data(self):
        data, client = self.server.recvfrom(1024)
        is_connection_event = self.parse_connection_events(data, client)

        if is_connection_event:
            return None, None
        return data, client

    def __send_data(self, data, client):
        self.server.sendto(data, client)

    def enc_and_send_data(self, data, client):
        enc_data = pickle.dumps(data)
        self.__send_data(enc_data, client)

    def broadcast_data(self, data, except_clients):
        clients_to_send = set(self.clients) - set(except_clients)
        for client in clients_to_send:
            self.__send_data(data, client)

    def enc_and_broadcast_data(self, data, except_clients):
        enc_data = pickle.dumps(data)
        self.broadcast_data(enc_data, except_clients)

    def parse_connection_events(self, data, client):
        dec_data = pickle.loads(data)
        if dec_data == NetworkEvents.CONNECT.value:
            if self.should_connect(self, client):
                print(f"[CONNECTED] {client}")
                self.clients.add(client)
                print(f"{len(self.clients)} clients available")
                self.on_connect(self, client)
            else:
                print(f"[CONNECTION REFUSED] {client}")
            return True

        if dec_data == NetworkEvents.DISCONNECT.value:
            print(f"[DISCONNECTED] {client}")
            self.clients.remove(client)
            print(f"{len(self.clients)} clients available")
            self.on_disconnect(self, client)
            return True

        return False
