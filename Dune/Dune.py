import tkinter as tk
from random import randint


class Arc:
    def __init__(self, canvas):
        self.x = 700
        self.y = 500
        self.deltaX = 300
        self.deltaY = 200
        self.duneCanvas = canvas
        self.drawArc()
    
    def drawArc(self):
        self.canvObj = self.duneCanvas.create_arc(
            self.x,
            self.y,
            self.x + self.deltaX,
            self.y + self.deltaY,
            start=-150, extent=120, style=tk.ARC)
        self.duneCanvas.create_text(self.x, self.y, text="X")
        self.duneCanvas.create_text(self.x+self.deltaX, self.y+self.deltaY, text="X")
        



class Dune:
    def __init__(self, master):
        self.master = master
        self.master.title("Dune")
        self.master.geometry("800x800")

        # Initialising Tkinter Variables
        self.frame = tk.Frame(self.master, width=800, height=800)
        self.canvas = tk.Canvas(self.frame, width=800, height=800, bg="lightblue")
        self.canvas.bind("<space>", self.onSpace)

        self.arcs = []
        self.refreshDelay = 10

    def onSpace(self, event):
        self.spawnNewArc()

    def spawnNewArc(self):
        newArc = Arc(self.canvas)
        self.arcs.append(newArc)

    def draw(self):
        # Initialise canvas
        self.frame.pack()
        self.canvas.pack()
        self.canvas.focus_set()

        self.refreshAgain = True
        self.refresh()

    def refresh(self):
        for arc in self.arcs:
            self.canvas.move(arc.canvObj, -1, 0)


        self.master.update()
        if self.refreshAgain:
            self.master.after(self.refreshDelay,self.refresh)





if __name__ == '__main__':
    root = tk.Tk()

    app = Dune(root)
    app.draw()

    root.mainloop()