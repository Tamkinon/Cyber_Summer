import socket

LENGTH_FIELD_SIZE = 4

my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 5555))
print("Connected to the server.")

while True:
    name = input("Enter Name:   ")
    my_socket.send(name.encode())

    data = my_socket.recv(1024).decode()
    print(data)
