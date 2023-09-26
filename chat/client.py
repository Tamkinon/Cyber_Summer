import socket
import tkinter as tk
from tkinter import ttk, scrolledtext
import select
from tkextrafont import Font
import textwrap

my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 5555))
print("Connected to the server.")

socket_messages = [my_socket]
my_msg = []


def send_message(msg_entry):
    message = msg_entry.get("1.0", "end-1c")
    my_socket.send(message.encode())
    create_message_box(message, "left", "aquamarine2")
    msg_entry.delete(1.0, tk.END)
    if message.lower() == "quit":
        root.destroy()


def receive_messages(text_widget):
    rlist, wlist, xlist = select.select(socket_messages, socket_messages, [])
    for sock in rlist:
        if sock is my_socket:
            msg = my_socket.recv(1024).decode()
            create_message_box(msg, "right", "gray82")  # Create a message box per message (e for east, w for west)


def create_message_box(message, side, colour):
    # bd (border width) - specifies the width of the border around the frame
    # relief - specifies the type of border or relief effect around the frame.
    # In this case, "solid" is used to create a solid border around the frame.
    # padx and pady -
    # specify the amount of empty space or padding to add around the content inside the frame.
    # wraplength specifies the maximum number of characters that can appear on a single line before the text is automatically wrapped to the next line.
    # justify specifies how the text should be aligned within its container.
    # "left" means the text is left-aligned within the Label widget, so it starts from the left edge and extends to the right as far as necessary.
    wrapper = textwrap.TextWrapper(width=37) # 70% = 44, 60% = 37
    message = wrapper.fill(text=message)

    expanding_message_frame = tk.Frame(chat_frame, relief="sunken", pady=5, bg="#e1fcf7")
    expanding_message_frame.pack(side="top", fill="x")

    message_frame = tk.Frame(expanding_message_frame, bd=1, relief="solid", bg=colour)
    message_frame.pack(side=side, padx=(4.5, 8))

    message_label = tk.Label(message_frame, text=message, justify="left", bg=colour, font=fnt)
    message_label.pack()


def on_canvas_configure(event):
    canvas.itemconfig("frame", width=canvas.winfo_width())  # Make the frame fill the canvas width
    canvas.config(scrollregion=canvas.bbox("all"))


# Create the main GUI window
root = tk.Tk()
root.title("Chat")
root.configure(bg="lightblue")
root.geometry("600x800")

# Font for all text
fnt = Font(file="VarelaRound-Regular.ttf", family="Varela round", size=15)

# Create a Canvas
container = tk.Frame(root, background="#e1fcf7")
container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
canvas = tk.Canvas(container, background="#e1fcf7")
canvas.pack(side="left", fill="both", expand=True)

# Create a scroll bar
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Frame for displaying messages
chat_frame = tk.Frame(canvas, background="#e1fcf7")
canvas.create_window((0, 0), window=chat_frame, anchor="nw", tags="frame")
chat_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# create a frame for user input and send button
input_frame = tk.Frame(root)
input_frame.pack(fill=tk.X, side=tk.TOP, anchor='s')

# Create a text entry widget for user input
message_entry = scrolledtext.ScrolledText(input_frame, height=2, width=5, font=fnt, wrap=tk.WORD)
message_entry.pack(side='left', fill='x', expand=True)

# Create a send button.
imgSend = tk.PhotoImage(file='send.png')
send_button = tk.Button(input_frame, text="Send", image=imgSend, command=lambda: send_message(message_entry))
send_button.pack(side='right')

# configure the canvas
canvas.bind("<Configure>", on_canvas_configure)
on_canvas_configure(None)


def check_for_messages():
    receive_messages(chat_frame)
    root.after(100, check_for_messages)


# Start checking for messages
check_for_messages()

# Main GUI loop
root.mainloop()
