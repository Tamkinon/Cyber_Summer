__author__ = 'Me'

import tkinter as tk
from tkinter import filedialog
import os
from tkextrafont import Font
import win32file
import socket

window = tk.Tk()

DL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Paths (Server - Desktop)
server_path = r'C:\Users\user\Desktop\Server Files'
desktop_path = r'C:\Users\user\Desktop'

# Fonts
fnt = Font(file="VarelaRound-Regular.ttf", family="Varela round", size=10)

# Colors
bg = "#f5f9fa"
button_bg = "#e3e7e8"

# String variables (Path variables)
var1 = tk.StringVar()
var2 = tk.StringVar()

# File types
audio_list = ["*.mp3", "*.m4a", "*.wav"]
image_list = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg", "*.tiff"]
video_list = ["*.mp4", "*.avi", "*.mov"]
text_list = ["*.txt", "*.doc", "*.docx"]

file_types = (("text files", text_list), ("image file", image_list),
              ("video files", video_list), ("audio files", audio_list))

# Settings
button_settings = {"height": 2, "width": 30, "font": fnt, "fg": "black", "bg": button_bg, "relief": "solid",
                   "border": 1}

label_settings = {"height": 1, "width": 72, "font": fnt, "bg": "White", "relief": "solid", "border": 1, "anchor": "w"}

# Texts
button_texts = ["Download the files from the Server", "Upload a file to the Server",
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

# open connection
my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 8830))


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

    # !
    if var1.get() != "" and var2.get() != "":  # if the user selected a file and a place to save it
        save_button.configure(state=tk.ACTIVE)
    else:  # the user didn't select a file or a place to save
        save_button.configure(state=tk.DISABLED)


def open_dialog_usb(from_path, to_path, index1, index2):
    """
    The function creates a file dialog - usb
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


def open_dialog_send():
    """
    The function creates a file dialog - server
    """
    file_name = filedialog.askopenfilename()  # opens file dialog #1

    # התחל בתיקיית הבתים שבה אתה רוצה לחפש את הקובץ
    file_path_to_send = file_name
    check = True

    def find_first_matching_file(base_directory, file_name, valid_extensions):
        for root, dirs, files in os.walk(base_directory):
            for file in files:
                if file.startswith(file_name) and any(file.lower().endswith(ext) for ext in valid_extensions):
                    return os.path.join(root, file)

    if not os.path.exists(file_name):
        check = False
        base_directory = "/"
        valid_extensions = ['.mp3', '.m4a', '.wav', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.tiff', '.mp4', '.avi',
                            '.mov', '.txt', '.doc', '.docx']

        file_path_to_send = find_first_matching_file(base_directory, file_name, valid_extensions)

    print(file_path_to_send)

    # שליחת שם הקובץ לשרת
    if file_path_to_send != "":
        my_socket.send("send".encode())
        with open(file_path_to_send, 'rb') as file:
            if not check:
                file_name = file_path_to_send[1:].split('\\')[-1]
            else:
                file_name = file_path_to_send.split('/')[-1]
            my_socket.send(file_name.encode())

            # שליחת תוכן הקובץ
            data = file.read(1024)
            while data:
                my_socket.send(data)
                data = file.read(1024)
            my_socket.send("end".encode())


def open_dialog_download():
    """
    The function creates a file dialog - server
    """
    target_directory = r"server's files"
    my_socket.send("download".encode())
    # קריאת מספר הקבצים בתיקייה
    num_files = int(my_socket.recv(1024).decode())

    # קריאת שמות הקבצים
    file_names = []
    for i in range(num_files):
        file_name = my_socket.recv(1024).decode()
        file_names.append(file_name)
        print(file_name)

    # יצירת התיקייה במחשב הלקוח
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # הורדת כל קובץ אחד אחרי השני
    for file_name in file_names:
        with open(os.path.join(target_directory, file_name), 'wb') as file:
            data = my_socket.recv(1024)
            while "endend".encode() not in data:
                file.write(data)
                data = my_socket.recv(1024)


def save_file(file_name):
    """
    The function saves the user's file in the selected place
    """
    with open(var1.get(), 'rb') as file1, \
            open(var2.get() + "\\" + file_name, 'wb') as file2:
        file2.write(file1.read())


def main():
    """

    :return:
    """
    # Initiate window and frame
    window.title("File Manager")
    window.geometry("600x290+685+480")
    window.resizable(width=tk.FALSE, height=tk.FALSE)
    window.configure(bg=bg)
    window.rowconfigure(ROWS)
    window.columnconfigure(COLUMNS)
    frame = tk.Frame(window, bg=bg)
    frame.pack()

    # Labels
    usb_label = tk.Label(window, text="No USB was found", font=fnt, bg=bg)
    label1 = tk.Label(window, text="Download/Upload From USB: ", font=fnt, bg=bg)
    label2 = tk.Label(window, text="Download/Upload To USB : ", font=fnt, bg=bg)
    label3 = tk.Label(window, label_settings, textvariable=var1)
    label4 = tk.Label(window, label_settings, textvariable=var2)

    # Packing Labels
    usb_label.pack(side=tk.BOTTOM)
    label1.pack(anchor="w", side=tk.TOP, pady=label_pad_y, padx=label_pad_x)
    label3.pack(anchor="w", side=tk.TOP, pady=0, padx=label_pad_x + 1)
    label2.pack(anchor="w", side=tk.TOP, pady=label_pad_y, padx=label_pad_x)
    label4.pack(anchor="w", side=tk.TOP, pady=0, padx=label_pad_x + 1)

    # Buttons
    download_button = tk.Button(frame, button_settings, text=button_texts[0],
                                command=lambda: open_dialog_download())

    upload_button = tk.Button(frame, button_settings, text=button_texts[1],
                              command=lambda: open_dialog_send())

    download_usb_button = tk.Button(frame, button_settings, text=button_texts[2],
                                    command=lambda: open_dialog_usb(check_for_usb_type()[1], desktop_path, 1, 4))

    upload_usb_button = tk.Button(frame, button_settings, text=button_texts[3],
                                  command=lambda: open_dialog_usb(desktop_path, check_for_usb_type()[1], 3, 5))

    save_button = tk.Button(window, height=1, width=10, text="Save", font=fnt, fg="black", bg=button_bg,
                            relief="solid", border=1, command=lambda: save_file(var1.get().split("/")[-1]))

    change_state(check_for_usb_type()[0], upload_usb_button, download_usb_button, usb_label, save_button)

    # Grid
    upload_button.grid(row=0, column=1, padx=button_pad_x, pady=button_pad_y)
    download_button.grid(row=0, column=0, padx=button_pad_x, pady=button_pad_y)
    upload_usb_button.grid(row=1, column=1, padx=button_pad_x, pady=button_pad_y)
    download_usb_button.grid(row=1, column=0, padx=button_pad_x, pady=button_pad_y)

    save_button.pack(side=tk.RIGHT, anchor="s", padx=button_pad_x + 1, pady=3)

    tk.mainloop()


if __name__ == '__main__':
    main()
