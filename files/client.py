__author__ = 'Me'

import tkinter as tk
from tkinter import filedialog
import os
from tkextrafont import Font
import win32file

DL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

window = tk.Tk()

var1 = tk.StringVar()
var2 = tk.StringVar()

audio_list = ["*.mp3", "*.m4a", "*.wav"]
image_list = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg", "*.tiff"]
video_list = ["*.mp4", "*.avi", "*.mov"]
text_list = ["*.txt", "*.doc", "*.docx"]

texts_list = ["Select a file you want to download from the Server",
              "Select a file you want to download from the USB",
              "Select a file you want to Upload to the Server",
              "Select a file you want to Upload to the USB",
              "Select where you want the file to be downloaded to",
              "Select where you want the file to be uploaded to"
              ]


def check_for_usb_type(drives_list):
    for drive in drives_list:
        if win32file.GetDriveType(drive) == 2:
            return True, drive
    return False, ''


def check_drives():
    drives = ['%s:' % d for d in DL if os.path.exists('%s:' % d)]
    # drives is a list with all the existing drives ('C:' / 'A:') on the computer (at the start of the script)
    usb_check, usb = check_for_usb_type(drives)
    return usb_check, usb


def change_state(check_usb, upload_usb_button, download_usb_button, label):
    window.after(100, lambda: change_state(check_drives()[0], upload_usb_button, download_usb_button, label))
    if check_usb:
        upload_usb_button.configure(state=tk.ACTIVE)
        download_usb_button.configure(state=tk.ACTIVE)
        label.config(text="")
    else:
        upload_usb_button.configure(state=tk.DISABLED)
        download_usb_button.configure(state=tk.DISABLED)
        label.config(text="No USB was found")


def open_dialog(initial_dir, index1, index2):
    window.filename = filedialog.askopenfilename(initialdir=r'{}'.format(initial_dir),
                                                 title=texts_list[index1],
                                                 filetypes=(("audio files", audio_list), ("image file", image_list),
                                                            ("video files", video_list), ("text files", text_list)))
    var1.set(window.filename)

    window.filename = filedialog.askopenfilename(initialdir=r'{}'.format(initial_dir),
                                                 title=texts_list[index2],
                                                 filetypes=(("audio files", audio_list), ("image file", image_list),
                                                            ("video files", video_list), ("text files", text_list)))
    var2.set(window.filename)


def main():
    """

    :return:
    """
    # Initiate window
    window.title("File explorer")
    window.geometry("600x280+685+480")
    window.resizable(width=tk.FALSE, height=tk.FALSE)
    window.configure(bg="#f5f9fa")

    frame = tk.Frame(window, bg="#f5f9fa")
    frame.pack()

    # variables
    pad_x = 12
    pad_y = 5
    rows, columns = 2, 1
    check_usb, usb = check_drives()

    window.rowconfigure(rows)
    window.columnconfigure(columns)

    # Fonts
    fnt = Font(file="VarelaRound-Regular.ttf", family="Varela round", size=10)

    # Labels
    usb_label = tk.Label(window, text="No USB was found", font=fnt, bg="#f5f9fa")
    label1 = tk.Label(window, text="Download/Upload From: ", font=fnt, bg="#f5f9fa")
    label2 = tk.Label(window, text="Download/Upload To : ", font=fnt, bg="#f5f9fa")
    label3 = tk.Label(window, textvariable=var1, font=fnt, bg="White", relief="solid", anchor="w",
                      border=1, width=72, height=1)
    label4 = tk.Label(window, textvariable=var2, font=fnt, bg="White", relief="solid", anchor="w",
                      border=1, width=72, height=1)

    # Packing Labels
    usb_label.pack(side=tk.BOTTOM)
    label1.pack(anchor="w", side=tk.TOP, pady=10, padx=pad_x)
    label3.pack(anchor="w", side=tk.TOP, pady=0, padx=pad_x + 1)
    label2.pack(anchor="w", side=tk.TOP, pady=10, padx=pad_x)
    label4.pack(anchor="w", side=tk.TOP, pady=0, padx=pad_x + 1)

    # Buttons
    download_button = tk.Button(frame, height=2, width=30, text="Download a file from the Server",
                                font=fnt, fg="black", bg="#e3e7e8", relief="solid", border=1,
                                command=lambda: open_dialog(usb, 0, 4))

    upload_button = tk.Button(frame, height=2, width=30, text="Upload a file to the Server",
                              font=fnt, fg="black", bg="#e3e7e8", relief="solid", border=1,
                              command=lambda: open_dialog(usb, 2, 5))

    download_usb_button = tk.Button(frame, height=2, width=30, text="Download a file from the USB", font=fnt,
                                    fg="black", bg="#e3e7e8", relief="solid", border=1,
                                    command=lambda: open_dialog(usb, 1, 4))

    upload_usb_button = tk.Button(frame, height=2, width=30, text="Upload a file to the USB", font=fnt, fg="black",
                                  bg="#e3e7e8", relief="solid", border=1,
                                  command=lambda: open_dialog(usb, 3, 5))

    change_state(check_usb, upload_usb_button, download_usb_button, usb_label)

    # Grid
    upload_button.grid(row=0, column=1, padx=pad_x, pady=pad_y)
    download_button.grid(row=0, column=0, padx=pad_x, pady=pad_y)
    upload_usb_button.grid(row=1, column=1, padx=pad_x, pady=pad_y)
    download_usb_button.grid(row=1, column=0, padx=pad_x, pady=pad_y)

    tk.mainloop()


if __name__ == '__main__':
    main()
