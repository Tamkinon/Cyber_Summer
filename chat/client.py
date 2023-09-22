import socket
import tkinter as tk
import select
from tkinter import font
from tkextrafont import Font

my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 5555))
print("Connected to the server.")

socket_messages = [my_socket]
my_msg = []


def send_message(msg_entry):
    message = msg_entry.get()
    my_socket.send(message.encode())
    msg_entry.delete(0, tk.END)  # added this to delete the text (obviously)


def receive_messages(text_widget):
    rlist, wlist, xlist = select.select(socket_messages, socket_messages, [])
    for sock in rlist:
        if sock is my_socket:
            msg = my_socket.recv(1024).decode()
            create_message_box(msg, "w")  # Create a message box per message (e for east, w for west)


def create_message_box(message, side):
    # bd (border width) - specifies the width of the border around the frame
    # relief - specifies the type of border or relief effect around the frame.
    # In this case, "solid" is used to create a solid border around the frame.
    # padx and pady -
    # specify the amount of empty space or padding to add around the content inside the frame.
    # wraplength specifies the maximum number of characters that can appear on a single line before the text is automatically wrapped to the next line.
    # justify specifies how the text should be aligned within its container.
    # "left" means the text is left-aligned within the Label widget, so it starts from the left edge and extends to the right as far as necessary.
    message_frame = tk.Frame(chat_frame, bd=1, relief="solid", padx=5, pady=5, bg="aquamarine2")
    message_frame.grid(sticky=side, pady=4)

    message_label = tk.Label(message_frame, text=message, wraplength=450, justify="left", bg="aquamarine2", font=fnt)
    message_label.pack()


# Create the main GUI window
root = tk.Tk()
root.title("Chat")
root.configure(bg="lightblue")
root.geometry("600x800")

# Font for all text
fnt = Font(file="VarelaRound-Regular.ttf", family="Varela round", size=20)

# Frame for displaying messages
chat_frame = tk.Frame(root)
chat_frame.pack(fill=tk.BOTH, expand=True)
chat_frame.configure(bg="mintcream")

# Create a text entry widget for user input
message_entry = tk.Entry(root, width=30, font=fnt)
message_entry.pack(fill=tk.BOTH, expand=False)

# Create a send button
imgSend = tk.PhotoImage(file='send.png')
send_button = tk.Button(root, text="Send", image=imgSend, command=lambda: send_message(message_entry))
send_button.pack()


def check_for_messages():
    receive_messages(chat_frame)
    root.after(100, check_for_messages)


# Start checking for messages
check_for_messages()

# Main GUI loop
root.mainloop()
