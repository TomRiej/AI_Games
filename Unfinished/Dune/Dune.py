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
        # move it on screen
        self.duneCanvas.move(self.canvObj, self.velocity, 0)
        self.x += self.velocity

     


class Ball:
    def __init__(self, canvas):
        self.x = 100
        self.y = 400
        self.xVel = 0
        self.yVel = 0

        self.radius = 20
        self.duneCanvas = canvas
        self.drawBall()

    def drawBall(self):
        self.canvObj = self.duneCanvas.create_oval(self.getBallDims(), fill="lightgreen")

    def getBallDims(self):
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        return x1,y1,x2,y2

    def move(self):
        # move on screen
        if self.y < 800:
            self.duneCanvas.move(self.canvObj, 0, self.yVel)
            self.y += self.yVel

        # acceleration due to gravity
        self.yVel += GRAVITY
        


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
        self.balls = []
        self.refreshDelay = 10

    def onSpace(self, event):
        self.spawnNewArc()

    def spawnNewBall(self):
        newBall = Ball(self.canvas)
        self.balls.append(newBall)

    def spawnNewArc(self):
        newArc = Arc(self.canvas)
        self.arcs.append(newArc)

    def checkCollisions(self, ballObj):
        self.canvas.find_overlapping(ballObj,0,0,0)

    def draw(self):
        # Initialise canvas
        self.frame.pack()
        self.canvas.pack()
        self.canvas.focus_set()

        # spawn starting line
        self.startLine = self.canvas.create_line(0,500,800,500)
        # spawn First arc and ball
        self.spawnNewBall()
        self.spawnNewArc()

        self.refreshAgain = True
        self.refresh()

    def refresh(self):
        for arc in self.arcs:
            arc.move()
            if arc.x + arc.deltaX < 0:
                self.canvas.delete(arc.canvObj)
                del arc

        for ball in self.balls:
            ball.move()

        

        recentArc = self.arcs[-1]
        if recentArc.x + recentArc.deltaX < 800:
            self.spawnNewArc()


        self.master.update()
        if self.refreshAgain:
            self.master.after(self.refreshDelay,self.refresh)

GRAVITY = 0.1



if __name__ == '__main__':
    root = tk.Tk()

    app = Dune(root)
    app.draw()

    root.mainloop()