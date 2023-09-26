__author__ = 'Me'

import tkinter as tk
import os
from tkextrafont import Font
import win32file

DL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

window = tk.Tk()


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


def main():
    """

    :return:
    """
    # Initiate window
    window.title("File explorer")
    window.geometry("550x150+685+480")
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
    label = tk.Label(window, text="No USB was found", font=fnt, bg="#f5f9fa")

    # Packing Labels
    label.pack(side=tk.BOTTOM)

    # Buttons
    upload_button = tk.Button(frame, height=2, width=30, text="Download a file from the Server",
                              font=fnt, fg="black", bg="#e3e7e8", relief="solid", border=1)

    download_button = tk.Button(frame, height=2, width=30, text="Upload a file to the Server",
                                font=fnt, fg="black", bg="#e3e7e8", relief="solid", border=1)
    upload_usb_button = tk.Button(frame, height=2, width=30, text="Download a file from the USB", font=fnt, fg="black",
                                  bg="#e3e7e8", relief="solid", border=1)

    download_usb_button = tk.Button(frame, height=2, width=30, text="Upload a file to the USB", font=fnt, fg="black",
                                    bg="#e3e7e8", relief="solid", border=1)

    change_state(check_usb, upload_usb_button, download_usb_button, label)

    # Grid
    upload_button.grid(row=0, column=0, padx=pad_x, pady=pad_y)
    download_button.grid(row=0, column=1, padx=pad_x, pady=pad_y)
    upload_usb_button.grid(row=1, column=0, padx=pad_x, pady=pad_y)
    download_usb_button.grid(row=1, column=1, padx=pad_x, pady=pad_y)

    tk.mainloop()


if __name__ == '__main__':
    main()
