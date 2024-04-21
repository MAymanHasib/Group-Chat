import socket
import threading

HOST = '0.0.0.0'
PORT = 9003


groups = {}

def handle_client(client_socket, client_address):
    print(f'Client {client_address} connected.')


    client_socket.sendall(b'Enter your username: ')
    username = client_socket.recv(1024).decode().strip()


    client_socket.sendall(b'Which group do you want to join? ')
    group_id = client_socket.recv(1024).decode().strip()


    if group_id not in groups:
        groups[group_id] = []


    groups[group_id].append((client_socket, username))

    while True:
        data = client_socket.recv(1024)

        if not data:
            break


        for group_client, group_client_username in groups[group_id]:
            if group_client != client_socket:
                message = f'{group_client_username}: {data.decode()}'
                group_client.sendall(message.encode())


    groups[group_id].remove((client_socket, username))
    print(f'Client {client_address} disconnected.')
    client_socket.close()

def accept_clients(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f'Server listening on {HOST}:{PORT}')

    accept_thread = threading.Thread(target=accept_clients, args=(server_socket,))
    accept_thread.start()
    accept_thread.join()
