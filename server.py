import socket


def start_server():
    server_ip = "127.0.0.1"
    server_port = 5555
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((server_ip, server_port))

    clients = set()
    print(f"[LISTENING] Server is listening on {server_ip}:{server_port}")

    while True:
        data, addr = server.recvfrom(1024)
        clients.add(addr)
        for client in clients:
            if client != addr:
                server.sendto(data, client)


if __name__ == "__main__":
    start_server()
