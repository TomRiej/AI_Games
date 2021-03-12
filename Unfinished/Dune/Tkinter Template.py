import tkinter as tk


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

    def setup(self):
        # Initialise canvas
        self.frame.pack()
        self.canvas.pack()
        self.canvas.focus_set()

    def update(self):
        self.canvas.delete("all")
        # draw everything this frame
        self.master.after(1, self.update)

SIZE = "800"

if __name__ == '__main__':
    root = tk.Tk()

    app = App(root)
    app.setup()
    app.update()

    root.mainloop()