import socket
import tkinter as tk
from tkinter import ttk, scrolledtext
import select
from tkextrafont import Font
import random
import datetime

my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 5555))
print("Connected to the server.")

socket_messages = [my_socket]
my_msg = []


def send_message(msg_entry):
    original_message = msg_entry.get("1.0", "end-1c")
    message = str(len(name)).zfill(2) + name + "1" + str(len(original_message)).zfill(4) + original_message
    my_socket.send(message.encode())
    msg_entry.delete(1.0, tk.END)
    if original_message.lower() == "quit":
        root.destroy()
    else:
        create_message_box(original_message, "left", "aquamarine2", name)


def receive_messages(text_widget):
    rlist, wlist, xlist = select.select(socket_messages, socket_messages, [])
    for sock in rlist:
        if sock is my_socket:
            name_length = my_socket.recv(2).decode()
            client_name = my_socket.recv(int(name_length)).decode()
            message_length = my_socket.recv(4).decode()
            data = my_socket.recv(int(message_length)).decode()
            if client_name == "Server":
                create_message_box(data, "top", "gray82", client_name)
            else:
                create_message_box(data, "right", "LightCyan3", client_name)


def create_message_box(message, side, colour, name):
    # bd (border width) - specifies the width of the border around the frame
    # relief - specifies the type of border or relief effect around the frame.
    # In this case, "solid" is used to create a solid border around the frame.
    # padx and pady -
    # specify the amount of empty space or padding to add around the content inside the frame.
    # wraplength specifies the maximum number of pixels that can appear on a single line before the text is automatically wrapped to the next line.
    # justify specifies how the text should be aligned within its container.
    # "left" means the text is left-aligned within the Label widget, so it starts from the left edge and extends to the right as far as necessary.

    expanding_message_frame = tk.Frame(chat_frame, relief="sunken", pady=5, bg="#e1fcf7")
    expanding_message_frame.pack(side="top", fill="x")

    message_frame = tk.Frame(expanding_message_frame, bd=1, relief="solid", bg=colour)
    message_frame.pack(side=side, padx=(4.5, 8))

    name_label = tk.Label(message_frame, text=name, font=("Arial", 14), justify="left", bg=colour, fg=random_colour(name))
    name_label.pack(anchor="w")

    message_label = tk.Label(message_frame, text=message, justify="left", bg=colour, font=fnt, wraplength=450)
    message_label.pack(anchor="w")

    time_label = tk.Label(message_frame, text=update_time(), font=("Arial", 12), justify="left", bg=colour)
    time_label.pack(anchor="e")


def on_canvas_configure(event):
    canvas.itemconfig("frame", width=canvas.winfo_width())  # Make the frame fill the canvas width
    canvas.config(scrollregion=canvas.bbox("all"))
    # canvas.yview_moveto(1.0)


def random_colour(name):
    random.seed(name)
    color = random.randrange(0, 2 ** 16)
    hex_color = hex(color)
    colour_string = "#" + hex_color[2:4] + "00" + hex_color[-2:]
    return colour_string


def update_time():
    return datetime.datetime.now().strftime("%H:%M")


def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")


name = input("What is your name? ")
name_colour = random_colour(name)


# Create the main GUI window
root = tk.Tk()
root.resizable(width=False, height=False)
root.title(name + "'s Chat")
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
canvas.bind_all("<MouseWheel>", on_mousewheel)
canvas.configure(yscrollcommand=scrollbar.set)

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
