import tkinter as tk
from random import randint


# ===================================== Main Game Class =======================


class Twist():
    def __init__(self, master):
        self.master = master
        self.master.title("Twist")
        self.master.geometry("800x800")



if __name__ == '__main__':
    root = tk.Tk()

    app = Twist(root)

    root.mainloop()