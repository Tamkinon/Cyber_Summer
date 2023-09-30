import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = '0.0.0.0'


def print_client_sockets(clients):
    for c in clients:
        print("\t", c.getpeername())


print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")

client_sockets = []
messages_to_send = []


while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            print_client_sockets(client_sockets)
        else:
            name_length = current_socket.recv(2).decode()
            client_name = current_socket.recv(int(name_length)).decode()
            client_command = current_socket.recv(1).decode()
            message_length = current_socket.recv(4).decode()
            data = current_socket.recv(int(message_length)).decode()
            if data == "quit":
                print("Connection closed", current_socket.getpeername())
                data = client_name + " has left the chat!"
                message = "6".zfill(2) + "Server" + str(len(data)).zfill(4) + data
                messages_to_send.append((current_socket, client_sockets, message))
                #current_socket.recv(MAX_MSG_LENGTH).decode()
                client_sockets.remove(current_socket)
                current_socket.close()
                print_client_sockets(client_sockets)
            else:
                message = name_length.zfill(2) + client_name + message_length.zfill(4) + data
                messages_to_send.append((current_socket, client_sockets, message))

    for message in messages_to_send:
        for receiver_socket in client_sockets:
            sender_socket, client_sockets, data = message
            if sender_socket in wlist and receiver_socket is not sender_socket:
                print(data)
                receiver_socket.send(data.encode())
        messages_to_send.remove(message)

