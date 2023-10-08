__author__ = 'Me'

import socket
import os

SERVER_PORT = 8830
SERVER_IP = '0.0.0.0'


def save_file(file_path, save_path):
    """
    The function saves the user's file in the selected place
    """
    with open(file_path, 'rb') as file1, \
            open(save_path + "\\" + file_path.split("/")[-1], 'wb') as file2:
        file2.write(file1.read())


def check_file(file_path, save_path):
    if os.path.exists(save_path + "\\" + file_path.split("/")[-1]):
        return "File already exists", False
    else:
        return "File can be saved", True


def main():

    run = True

    print("Setting up server...")
    server_socket = socket.socket()
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Server is up and running !")

    client_socket, client_address = server_socket.accept()
    print("Client connected.")

    while run:
        command = client_socket.recv(1).decode()
        if command == "0":  # 0 = client sent a file-path message
            file_length = client_socket.recv(4).decode()
            file_path = client_socket.recv(int(file_length)).decode()
            save_length = client_socket.recv(4).decode()
            save_path = client_socket.recv(int(save_length)).decode()

            message = check_file(file_path, save_path)
            full_message = str(len(message[0].encode())).zfill(4) + message[0]
            if message[1]:
                save_file(file_path, save_path)
            client_socket.send(full_message.encode())

        elif command == "9":  # 9 = client sent a closing message
            run = False  # close loop

    client_socket.close()  # close client socket
    server_socket.close()  # close server socket
    print("Server closed.")


if __name__ == '__main__':
    main()
