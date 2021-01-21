import tkinter as tk
from random import randint

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("App Name")
        self.master.geometry(SIZE+"x"+SIZE)

        # Initialising Tkinter Variables
        self.frame = tk.Frame(self.master, width=800, height=800)
        self.canvas = tk.Canvas(self.frame, width=800, height=800, bg="lightblue")
        self.canvas.bind("<space>", self.onSpace)

    def onSpace(self, event):
        print("space")

    def draw(self):
        # Initialise canvas
        self.frame.pack()
        self.canvas.pack()
        self.canvas.focus_set()

SIZE = "800"

if __name__ == '__main__':
    root = tk.Tk()

    app = App(root)
    app.draw()

    root.mainloop()