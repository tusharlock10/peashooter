import pickle
import socket
import threading

from constants import NetworkEvents


class ClientNetwork:
    def __init__(self):
        self.client = None
        self.client_id = None
        self.server_ip = "127.0.0.1"
        self.server_port = 5555

    def create_connection(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_id = id(self.client)
        self.send_data(NetworkEvents.CONNECT.value)

    def __data_thread(self, receiver_func):
        while True:
            try:
                enc_data, _ = self.client.recvfrom(1024)
                data = pickle.loads(enc_data)
                receiver_func(data)
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    def receive_data(self, receiver_func):
        t = threading.Thread(target=self.__data_thread, args=[receiver_func])
        t.start()

    def send_data(self, data):
        enc_data = pickle.dumps(data)
        self.client.sendto(enc_data, (self.server_ip, self.server_port))

    def close(self):
        self.send_data(NetworkEvents.DISCONNECT.value)
        self.client.close()
