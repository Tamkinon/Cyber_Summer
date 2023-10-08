from tkinter import messagebox
from tkinter import *


class ColorButton:
    global square_length
    __current_color = "black"

    def __init__(self, root, color_type):
        self.__root = root
        self.__color_type = color_list1[color_type]
        self.__text = str(color_type)
        self.__button = Button(self.__root, text=self.__text, command=lambda: self.color())

    def color(self):
        if ColorButton.__current_color == self.__color_type:
            self.__button.configure(bg=ColorButton.__current_color, text="")

    @staticmethod
    def set_current_color(new_color):
        ColorButton.__current_color = new_color

    def get_color_type(self):
        return self.__color_type

    def get_text(self):
        return self.__text

    def get_button(self):
        return self.__button


color_list1 = ['white', 'black', 'light grey', 'red', 'red4', 'orange', 'green2', 'green4', 'yellow', 'blue']
square_length = 30
color_square_length = 50
default_height_pixels = 26
default_width_pixels = 17

current_color = "black"


# the pictures
picture_matrix1 = [[0, 0, 0, 7, 7, 0, 0, 0, 0, 0],
                   [0, 0, 7, 7, 7, 7, 0, 6, 6, 0],
                   [0, 7, 7, 7, 7, 7, 7, 6, 1, 6],
                   [0, 7, 7, 7, 7, 7, 7, 6, 6, 6],
                   [7, 7, 7, 7, 7, 7, 7, 6, 6, 0],
                   [0, 6, 6, 6, 6, 6, 6, 0, 0, 0],
                   [0, 6, 6, 0, 0, 6, 6, 0, 0, 0],
                   ]

picture_matrix2 = [[1, 1, 1, 8, 8, 5, 5, 1, 1, 1],
                   [1, 1, 8, 9, 8, 5, 9, 5, 1, 1],
                   [1, 1, 8, 9, 3, 3, 9, 5, 1, 1],
                   [1, 8, 3, 3, 3, 3, 3, 3, 5, 1],
                   [1, 8, 8, 3, 3, 3, 3, 5, 5, 1],
                   [1, 8, 8, 8, 8, 5, 5, 5, 5, 1],
                   [1, 8, 8, 8, 8, 5, 5, 5, 5, 1],
                   [1, 1, 8, 8, 5, 5, 5, 5, 1, 1],
                   [1, 1, 3, 5, 5, 5, 5, 3, 1, 1],
                   [1, 3, 3, 3, 1, 1, 3, 3, 3, 1],
                   ]

picture_matrix3 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 2, 2, 1, 4, 0, 4, 3, 0, 0],
                   [0, 0, 4, 1, 0, 0, 0, 5, 5, 0, 2, 2, 4, 3, 4, 3, 4, 3, 0],
                   [0, 1, 3, 4, 3, 4, 3, 0, 0, 0, 2, 4, 3, 1, 1, 4, 3, 0, 0],
                   [0, 1, 1, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 1, 1, 0, 4, 3, 0],
                   [0, 1, 1, 0, 0, 0, 3, 4, 3, 4, 3, 4, 2, 1, 1, 0, 0, 0, 0],
                   [0, 1, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0],
                   [0, 0, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0, 0, 0, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 5, 5, 1, 1, 1, 1, 5, 5, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   ]


def create_root(name):
    root = Tk(className=name)
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d+%d+%d" % (int(w), int(h), 0, 0))
    root.resizable(width=False, height=False)
    return root


def change_color(c, color_indicator):
    global current_color
    current_color = c
    color_indicator.configure(bg=current_color)
    ColorButton.set_current_color(current_color)


def color_all(buttons):
    for obj in buttons:
        obj.get_button().configure(bg=obj.get_color_type(), text="")


def remove_all_color(buttons):
    for obj in buttons:
        obj.get_button().configure(bg="SystemButtonFace", text=obj.get_text())


def submit(buttons, root):
    check = True
    i = 0
    while i < len(buttons) and check:
        check = check and buttons[i].get_color_type() == buttons[i].get_button().cget('bg')
        i += 1
    if check:
        messagebox.showinfo("congratulations", "you finished coloring the picture!", parent=root)
    else:
        messagebox.showinfo("oops", "the picture isn't completely colored!", parent=root)


def return_to_menu(root):
    root.destroy()
    main()


def print_picture(picture_matrix, root1):
    global square_length
    square_length = root1.winfo_screenheight()*0.5 / len(picture_matrix)
    x = 0
    y = 0

    frame = Frame(root1, width=len(picture_matrix[0])*square_length, height=len(picture_matrix)*square_length)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    all_buttons = []

    for i in range(len(picture_matrix)):
        for j in range(len(picture_matrix[i])):
            b = ColorButton(frame, picture_matrix[i][j])
            all_buttons.append(b)
            b.get_button().place(x=x, y=y, width=square_length, height=square_length)
            x += square_length
        y += square_length
        x = 0
    return all_buttons


def create_buttons(root1, buttons):
    color_label = Label(root1, text="current color:", font=25)
    color_canvas = Canvas(root1, width=color_square_length, height=color_square_length, bg=current_color)

    shared_parameters = color_canvas

    white = Button(root1, command=lambda: change_color("white", shared_parameters), bg="white", text=0)
    black = Button(root1, command=lambda: change_color("black", shared_parameters), bg="black", text=1, fg="white")
    light_grey = Button(root1, command=lambda: change_color("light grey", shared_parameters), bg="light grey", text=2)
    red = Button(root1, command=lambda: change_color("red", shared_parameters), bg="red", text=3)
    dark_red = Button(root1, command=lambda: change_color("red4", shared_parameters), bg="red4", text=4)
    orange = Button(root1, command=lambda: change_color("orange", shared_parameters), bg="orange", text=5)
    green2 = Button(root1, command=lambda: change_color("green2", shared_parameters), bg="green2", text=6)
    green4 = Button(root1, command=lambda: change_color("green4", shared_parameters), bg="green4", text=7)
    yellow = Button(root1, command=lambda: change_color("yellow", shared_parameters), bg="yellow", text=8)
    blue = Button(root1, command=lambda: change_color("blue", shared_parameters), bg="blue", text=9)

    color_list = [white, black, light_grey, red, dark_red, orange, green2, green4, yellow, blue]

    color_all_button = Button(root1, command=lambda: color_all(buttons), text="color all", font="arial 15",
                              bg='white')
    remove_all_color_button = Button(root1, command=lambda: remove_all_color(buttons), text="remove all color",
                                     font="arial 15", bg='white')
    submit_button = Button(root1, command=lambda: submit(buttons, root1), text="submit", bg='white', font="arial 40")
    menu_button = Button(root1, command=lambda: return_to_menu(root1), text="menu", bg="light blue", font="arial 40")

    x = 0.5/len(color_list)
    for i in color_list:
        i.place(relx=x, rely=0.1, width=color_square_length, height=color_square_length, anchor=CENTER)
        x += 1/len(color_list)
    color_label.place(relx=0.1, rely=0.2, height=20, width=120, anchor=CENTER)
    color_canvas.place(relx=0.2, rely=0.2, anchor=CENTER)
    color_all_button.place(relx=0.1, rely=0.3, width=color_square_length*3, height=color_square_length, anchor=CENTER)
    remove_all_color_button.place(relx=0.2, rely=0.3, width=color_square_length*3, height=color_square_length,
                                  anchor=CENTER)
    submit_button.place(relx=0.8, rely=0.5, width=color_square_length*5, height=color_square_length*2, anchor=CENTER)
    menu_button.place(relx=0.1, rely=0.8, width=color_square_length*3, height=color_square_length*1, anchor=CENTER)


def picture1(menu):
    menu.destroy()
    root = create_root("picture 1")

    buttons = print_picture(picture_matrix1, root)

    create_buttons(root, buttons)

    root.mainloop()


def picture2(menu):
    menu.destroy()
    root = create_root("picture 2")

    buttons = print_picture(picture_matrix2, root)

    create_buttons(root, buttons)

    root.mainloop()


def picture3(menu):
    menu.destroy()
    root = create_root("picture 3")

    buttons = print_picture(picture_matrix3, root)

    create_buttons(root, buttons)

    root.mainloop()


def main():
    menu = Tk(className="color game menu")
    w = menu.winfo_screenwidth()
    h = menu.winfo_screenheight()
    menu.geometry("%dx%d+%d+%d" % (int(w / 2), int(h / 2), int(w / 4), int(h / 5)))
    menu.configure(bg="light blue")
    menu.resizable(width=False, height=False)

    button1 = Button(menu, text="First picture", bg="orange", command=lambda: picture1(menu), width=15)
    button2 = Button(menu, text="Second picture", bg="dark orange", command=lambda: picture2(menu), width=15)
    button3 = Button(menu, text="Third picture", bg="coral", command=lambda: picture3(menu), width=15)
    title = Label(menu, text="Color Game", bg="light blue", font="Times 60 italic bold")

    title.pack(expand=True)
    button1.pack(expand=True, anchor="n", ipadx=40, ipady=20)
    button2.pack(expand=True, anchor="n", ipadx=40, ipady=20)
    button3.pack(expand=True, anchor="n", ipadx=40, ipady=20)
    menu.mainloop()


main()
