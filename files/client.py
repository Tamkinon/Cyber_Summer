__author__ = 'Me'

import tkinter as tk
import os
from tkextrafont import Font

DL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def diff(list1, list2):
    """
    The function gets 2 lists and create a new list with the items from list 1 that aren't in list 2
    :param list1:
    :param list2:
    :return: returns a list
    :rtype: list
    """
    list_difference = [item for item in list1 if item not in list2]
    return list_difference


def check_for_usb_type():
    pass


def check_drives():
    drives = ['%s:' % d for d in DL if os.path.exists('%s:' % d)]
    # drives is a list with all the existing drives ('C:' / 'A:') on the computer (at the start of the script)
    print(drives)
    while True:
        unchecked_drives = ['%s:' % d for d in DL if os.path.exists('%s:' % d)]
        # unchecked_drives is a list like drives that contains all the drives on the computer
        x = diff(unchecked_drives, drives)  # x = a list with the drives that are in list 1 and not in list 2
        if x:  # if the list is not empty (a new drive was connected to the computer)
            print("New drives:     " + str(x))
            check_for_usb_type()
        x = diff(drives, unchecked_drives)  # x = a list with the drives that are in list 2 and not in list 1
        if x:  # if the list is not empty (a new drive was removed from the computer)
            print("Removed drives: " + str(x))
            pass
        drives = unchecked_drives  # update the drives list


def main():
    """

    :return:
    """

    # Initiate window
    window = tk.Tk()
    window.title("File explorer")
    window.geometry("550x150+685+480")
    window.resizable(width=tk.FALSE, height=tk.FALSE)
    frame = tk.Frame(window)
    frame.pack()

    # variables
    pad_x = 12
    pad_y = 5
    rows, columns = 2, 1
    button_mode = tk.DISABLED

    window.rowconfigure(rows)
    window.columnconfigure(columns)

    # Fonts
    fnt = Font(file="VarelaRound-Regular.ttf", family="Varela round", size=10)

    # Labels
    label = tk.Label(window, text="No USB was found", font=fnt)

    # Packing Labels
    label.pack(side=tk.BOTTOM)

    # Buttons
    upload_button = tk.Button(frame, height=2, width=30, text="Download a file from the Server",
                              font=fnt, fg="black")

    download_button = tk.Button(frame, height=2, width=30, text="Upload a file to the Server",
                                font=fnt, fg="black")

    upload_dok_button = tk.Button(frame, height=2, width=30, text="Download a file from the USB",
                                  font=fnt, fg="black", state=button_mode)

    download_dok_button = tk.Button(frame, height=2, width=30, text="Upload a file to the USB",
                                    font=fnt, fg="black", state=button_mode)

    # Grid
    upload_button.grid(row=0, column=0, padx=pad_x, pady=pad_y)
    download_button.grid(row=0, column=1, padx=pad_x, pady=pad_y)
    upload_dok_button.grid(row=1, column=0, padx=pad_x, pady=pad_y)
    download_dok_button.grid(row=1, column=1, padx=pad_x, pady=pad_y)

    tk.mainloop()


if __name__ == '__main__':
    main()

