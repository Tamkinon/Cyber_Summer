import socket
import tkinter as tk
import select

LENGTH_FIELD_SIZE = 4

my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 5555))
print("Connected to the server.")

socket_messages = [my_socket]
my_msg = []


def send_message(msg_entry):
    message = msg_entry.get()
    my_socket.send(message.encode())


def receive_messages(text_widget):
    rlist, wlist, xlist = select.select(socket_messages, socket_messages, [])
    for sock in rlist:
        if sock is my_socket:
            msg = my_socket.recv(1024)
            text_widget.insert(tk.END, msg.decode() + "\n")


# Create the main GUI window
root = tk.Tk()
root.title("Chat")

# Text box for displaying messages
text1 = tk.Text(root, relief="sunken", borderwidth=5, width=60, height=25)
text1.pack()

# Create a text entry widget for user input
message_entry = tk.Entry(root)
message_entry.pack(fill=tk.BOTH, expand=True)

# Create a send button
send_button = tk.Button(root, text="Send", command=lambda: send_message(message_entry))
send_button.pack()


def check_for_messages():
    receive_messages(text1)
    root.after(1000, check_for_messages)


# Start checking for messages
check_for_messages()

# Main GUI loop
root.mainloop()



