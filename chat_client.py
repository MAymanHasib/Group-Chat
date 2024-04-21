import socket
import threading

HOST = 'localhost'
PORT = 9003


def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            print(data.decode())
        except ConnectionResetError:
            print('Disconnected from server.')
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    # Ask the user for their username
    username = input('Enter your username: ')

    # Send the username to the server
    client_socket.sendall(username.encode())

    # Ask the user which group they want to join
    group_id = input('Which group do you want to join? ')

    # Send the group ID to the server
    client_socket.sendall(group_id.encode())

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        # Ask the user for a message to send
        message = input('> ')

        if not message:
            break

        # Send the message to the server
        client_socket.sendall(message.encode())

    receive_thread.join()
