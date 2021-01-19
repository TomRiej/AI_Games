import tkinter as tk
from random import randint


class Ball():
    def __init__(self):
        self.x = 400
        self.y = 600
        self.radius = 20
        self.yVel = 0

    def getBallDims(self):
        x0 = self.x - self.radius
        y0 = self.y - self.radius
        x1 = self.x + self.radius
        y1 = self.y + self.radius
        return x0,y0,x1,y1

class FlatPlatform:
    def __init__(self):
        self.y = 400
        self.leftX = 360
        self.rightX = 440

    def l(self):
        pass

# ===================================== Main Game Class =======================


class Twist():
    def __init__(self, master):
        self.master = master
        self.master.title("Twist")
        self.master.geometry("800x800")

        # Initialising Tkinter Variables
        self.frame = tk.Frame(self.master, width=800, height=800)
        self.canvas = tk.Canvas(self.frame, width=800, height=800, bg="lightblue")
        self.canvas.bind("<space>", self.onSpace)

    def onSpace(self, event):
        print("space")

    def spawnBall(self):
        self.ball = Ball()
        self.canvBird = self.canvas.create_oval(self.ball.getBallDims(), fill="yellow")

    def drawPersPLines(self):
        line = self.canvas.create_line(360,400,300,800)
        line2 = self.canvas.create_line(440,400, 500, 800)
        self.mLine = self.canvas.create_line(300,400,500,400)

    def draw(self):
        # Initialise canvas
        self.frame.pack()
        self.canvas.pack()
        self.canvas.focus_set()

        self.spawnBall()
        self.drawPersPLines()



if __name__ == '__main__':
    root = tk.Tk()

    app = Twist(root)
    app.draw()

    root.mainloop()