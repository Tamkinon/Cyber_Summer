import socket

LENGTH_FIELD_SIZE = 4

my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 5555))
print("Connected to the server.")

while True:
    name = input("Please Enter Your Message:   ")
    message = str(len(name)).zfill(LENGTH_FIELD_SIZE) + name
    my_socket.send(message.encode())
    if name == "":
        break
    data = my_socket.recv(1024).decode()
    print("The Server Sent " + data)
