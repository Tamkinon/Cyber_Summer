__author__ = 'Me'

import socket
import tkinter as tk
from tkinter import filedialog
import os
from tkextrafont import Font
import win32file

IP = '127.0.0.1'
PORT = 8830

my_socket = socket.socket()
my_socket.connect((IP, PORT))
print("Connected to the server.")

window = tk.Tk()

DL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Paths (Server - Desktop)
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
server_path = desktop_path + "\\" + "Server Files"

# Fonts
fnt = Font(file="VarelaRound-Regular.ttf", family="Varela round", size=10)

# Colors
bg = "#f5f9fa"
button_bg = "#e3e7e8"

# String variables (Path variables)
var1 = tk.StringVar()
var2 = tk.StringVar()
var3 = tk.StringVar()

# File types
audio_list = ["*.mp3", "*.m4a", "*.wav"]
image_list = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg", "*.tiff"]
video_list = ["*.mp4", "*.avi", "*.mov"]
text_list = ["*.txt", "*.doc", "*.docx"]

file_types = (("image file", image_list), ("text files", text_list),
              ("video files", video_list), ("audio files", audio_list))

# Settings
button_settings = {"height": 2, "width": 30, "font": fnt, "fg": "black", "bg": button_bg, "relief": "solid",
                   "border": 1}

label_settings = {"height": 1, "width": 72, "font": fnt, "bg": "White", "relief": "solid", "border": 1, "anchor": "w"}

# Texts
button_texts = ["Download a file from the Server", "Upload a file to the Server",
                "Download a file from the USB", "Upload a file to the USB"]

title_texts = ["Select a file you want to download from the Server",
               "Select a file you want to download from the USB",
               "Select a file you want to upload to the Server",
               "Select a file you want to upload to the USB",
               "Select where you want the file to be downloaded to",
               "Select where you want the file to be uploaded to"]

# Variables
button_pad_x = 12
button_pad_y = 5
label_pad_x = 12
label_pad_y = 10
ROWS, COLUMNS = 2, 1
n = 7


def check_for_usb_type():
    """
    The function creates a list of drives from the computer drives ('A:' / 'B:'...), goes over all the
    drives in the list and returns True and the name of the drive that is a USB type (2).
    if the list doesn't have drives or doesn't have a USB type drive it returns False
    """
    drives = ['%s:' % d for d in DL if os.path.exists('%s:' % d)]
    # drives is a list with all the existing drives ('C:' / 'A:') on the computer (at the start of the script)
    for drive in drives:
        if win32file.GetDriveType(drive) == 2:  # if the drive is a USB type drive
            return True, drive
    return False, ''


def change_state(check_usb, upload_usb_button, download_usb_button, label, save_button):
    """
    The function changes the state of the button, from Active to Disabled
    """
    window.after(100, lambda: change_state(check_for_usb_type()[0], upload_usb_button,
                                           download_usb_button, label, save_button))
    if check_usb:  # if there is a USB connected
        upload_usb_button.configure(state=tk.ACTIVE)
        download_usb_button.configure(state=tk.ACTIVE)
        label.config(text="")
    else:  # there isn't a USB connected
        upload_usb_button.configure(state=tk.DISABLED)
        download_usb_button.configure(state=tk.DISABLED)
        label.config(text="No USB was found")

    if var1.get() != "" and var2.get() != "":  # if the user selected a file and a place to save it
        save_button.configure(state=tk.ACTIVE)
    else:  # the user didn't select a file or a place to save
        save_button.configure(state=tk.DISABLED)


def open_dialog(from_path, to_path, index1, index2):
    """
    The function creates a file dialog
    """
    window.filename = filedialog.askopenfilename(initialdir=r'{}'.format(from_path), title=title_texts[index1],
                                                 filetypes=file_types)  # opens file dialog #1
    var1.set(window.filename)  # show the specified path
    if var1.get() != "":  # if the user did choose a file/place to save it
        window.filename = filedialog.askdirectory(initialdir=r'{}'.format(to_path),
                                                  title=title_texts[index2])  # opens file dialog #2
        var2.set(window.filename)  # show the specified path
        if var2.get() == "":  # if the user didn't choose a file/place to save it
            var1.set("")  # delete the other specified path


def send_file_to_server(file, path):
    message = "0" + str(len(file.encode())).zfill(4) + file + str(len(path.encode())).zfill(4) + path
    my_socket.send(message.encode())
    change_variables()
    receive_message()


def change_variables():
    """
    The function sets the variables according to the user actions
    """
    var1.set("")
    var2.set("")
    for i in range(n):
        change_label(i)


def change_label(index):
    window.after(index*300, lambda: var3.set("Saving File" + (index % 3 + 1) * "."))


def receive_message():
    message_length = my_socket.recv(4).decode()
    message = my_socket.recv(int(message_length)).decode()
    if message == "File already exists":
        window.after(300 * n, lambda: var3.set("The file already exists in the specified path !"))
    if message == "File can be saved":
        window.after(300 * n, lambda: var3.set("File Saved Successfully !"))


def create_server_folder():
    if not os.path.exists(server_path):  # if the server folder doesn't exist on the desktop
        os.mkdir(server_path)
    create_sub_folders()


def create_sub_folders():
    """
    The function creates sub folders
    """
    if not os.path.exists(server_path + "\\" + "Image Files"):
        os.mkdir(server_path + "\\" + "Image Files")
    if not os.path.exists(server_path + "\\" + "Audio Files"):
        os.mkdir(server_path + "\\" + "Audio Files")
    if not os.path.exists(server_path + "\\" + "Text Files"):
        os.mkdir(server_path + "\\" + "Text Files")
    if not os.path.exists(server_path + "\\" + "Video Files"):
        os.mkdir(server_path + "\\" + "Video Files")


def main():
    # Initiate window and frame
    create_server_folder()
    window.title("File Manager")
    window.geometry("600x320+685+480")
    window.resizable(width=tk.FALSE, height=tk.FALSE)
    window.configure(bg=bg)
    window.rowconfigure(ROWS)
    window.columnconfigure(COLUMNS)
    frame = tk.Frame(window, bg=bg)
    frame.pack()

    # Labels
    usb_label = tk.Label(window, text="No USB was found", font=fnt, bg=bg)
    label1 = tk.Label(window, text="Download/Upload From: ", font=fnt, bg=bg)
    label2 = tk.Label(window, text="Download/Upload To : ", font=fnt, bg=bg)
    label3 = tk.Label(window, label_settings, textvariable=var1)
    label4 = tk.Label(window, label_settings, textvariable=var2)
    label5 = tk.Label(window, textvariable=var3, font=fnt, bg=bg, anchor="w", width=72)

    # Packing Labels
    usb_label.pack(side=tk.BOTTOM)
    label1.pack(anchor="w", side=tk.TOP, pady=label_pad_y, padx=label_pad_x)
    label3.pack(anchor="w", side=tk.TOP, padx=label_pad_x + 1)
    label2.pack(anchor="w", side=tk.TOP, pady=label_pad_y, padx=label_pad_x)
    label4.pack(anchor="w", side=tk.TOP, padx=label_pad_x + 1)
    label5.pack(anchor="w", side=tk.TOP, pady=6, padx=label_pad_x + 1)

    # Buttons
    download_button = tk.Button(frame, button_settings, text=button_texts[0],
                                command=lambda: open_dialog(server_path, desktop_path, 0, 4))

    upload_button = tk.Button(frame, button_settings, text=button_texts[1],
                              command=lambda: open_dialog(desktop_path, server_path, 2, 5))

    download_usb_button = tk.Button(frame, button_settings, text=button_texts[2],
                                    command=lambda: open_dialog(check_for_usb_type()[1], desktop_path, 1, 4))

    upload_usb_button = tk.Button(frame, button_settings, text=button_texts[3],
                                  command=lambda: open_dialog(desktop_path, check_for_usb_type()[1], 3, 5))

    save_button = tk.Button(window, height=1, width=10, text="Save", font=fnt, fg="black", bg=button_bg,
                            relief="solid", border=1, command=lambda: send_file_to_server(var1.get(), var2.get()))

    change_state(check_for_usb_type()[0], upload_usb_button, download_usb_button, usb_label, save_button)

    # Grid
    upload_button.grid(row=0, column=1, padx=button_pad_x, pady=button_pad_y)
    download_button.grid(row=0, column=0, padx=button_pad_x, pady=button_pad_y)
    upload_usb_button.grid(row=1, column=1, padx=button_pad_x, pady=button_pad_y)
    download_usb_button.grid(row=1, column=0, padx=button_pad_x, pady=button_pad_y)

    save_button.pack(side=tk.RIGHT, anchor="s", padx=button_pad_x + 1)

    tk.mainloop()

    my_socket.send("9".encode())  # 9 = close both sockets
    print("Disconnected from the server.")


if __name__ == '__main__':
    main()
