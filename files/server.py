__author__ = 'Me'

import socket
import os
import shutil


def main():

    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8830))
    server_socket.listen(1)

    source_directory = r"client's files"
    os.mkdir(source_directory)

    client_socket, client_address = server_socket.accept()

    while True:

        def download():
            """
             שמירה של הקובץ שנשלח מהלקוח בתיקייה אצל השרת
            """
            # קריאה של שם הקובץ
            file_name = client_socket.recv(1024).decode()

            # פתח קובץ לשמירה
            with open(f'{source_directory}/{file_name}', 'wb') as file:
                data = client_socket.recv(1024)
                while "end".encode() not in data:
                    file.write(data)
                    data = client_socket.recv(1024)

        def send():
            """
            שליחת הקבצים שבתיקייה שיש בה את כל הקבצים שהלקוח שלח, אל הלקוח
            :return:
            """
            # שליחת מספר הקבצים בתיקייה
            files_to_send = os.listdir(source_directory)
            client_socket.send(str(len(files_to_send)).encode())

            # שליחת שמות הקבצים
            for file_name in files_to_send:
                print(file_name)
                client_socket.send(file_name.encode())

            # שליחת כל קובץ בנפרד
            for file_name in files_to_send:
                file_path = os.path.join(source_directory, file_name)
                with open(file_path, 'rb') as file:
                    data = file.read(1024)
                    while data:
                        client_socket.send(data)
                        data = file.read(1024)
                client_socket.send("endend".encode())

        message = client_socket.recv(1024).decode()
        if message == "send":
            download()
        if message == "download":
            send()


if __name__ == '__main__':
    main()
