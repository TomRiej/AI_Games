import tkinter as tk
from random import randint


class Arc:
    def __init__(self, canvas):
        self.x = 800
        self.y = 500
        self.deltaX = randint(50,400)
        self.deltaY = 250
        self.duneCanvas = canvas
        self.velocity = -2
        self.drawArc()
    
    def drawArc(self):
        self.canvObj = self.duneCanvas.create_arc(
            self.x,
            self.y,
            self.x + self.deltaX,
            self.y + self.deltaY,
            start=-180, extent=180, style=tk.ARC)
        self.duneCanvas.create_text(self.x, self.y, text="X")
        self.duneCanvas.create_text(self.x+self.deltaX, self.y+self.deltaY, text="X")

    def move(self):
        self.duneCanvas.move(self.canvObj, self.velocity, 0)
        self.x += self.velocity
        



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
        self.spawnNewArc()

        self.refreshAgain = True
        self.refresh()

    def refresh(self):
        for arc in self.arcs:
            arc.move()
            if arc.x + arc.deltaX < 0:
                self.canvas.delete(arc.canvObj)
                del arc

        recentArc = self.arcs[-1]
        if recentArc.x+ recentArc.deltaX <800:
            self.spawnNewArc()


        self.master.update()
        if self.refreshAgain:
            self.master.after(self.refreshDelay,self.refresh)





if __name__ == '__main__':
    root = tk.Tk()

    app = Dune(root)
    app.draw()

    root.mainloop()