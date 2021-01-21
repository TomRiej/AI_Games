import tkinter as tk
from random import randint

class Player:
    def __init__(self, canvas):
        self.mainCanvas = canvas
        self.x = 400
        self.y = 400
        self.yVel = 0
        self.size = 50
        self.draw()
    
    def draw(self):
        self.canvasObject = self.mainCanvas.create_rectangle(self.getDims(),fill="grey")

    def getDims(self):
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.size
        y2 = self.y + self.size
        return x1, y1, x2, y2

    def fall(self):
        self.mainCanvas.move(self.canvasObject, 0, self.yVel)
        self.y += self.yVel
        self.yVel += GRAVITY

    def jump(self):
        self.yVel = 0
        self.yVel += JUMP_STRENGTH
        self.mainCanvas.move(self.canvasObject, 0, self.yVel)
        self.y += self.yVel


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("App Name")
        self.master.geometry(SIZE+"x"+SIZE)

        # Initialising Tkinter Variables
        self.frame = tk.Frame(self.master, width=800, height=800)
        self.canvas = tk.Canvas(self.frame, width=800, height=800, bg="LightGrey")
        self.canvas.bind("<Up>", self.onUp)

    def onUp(self, event):
        self.players[0].jump()

    def spawnPlayer(self):
        newPlayer = Player(self.canvas)
        self.players.append(newPlayer)

    def draw(self):
        # Initialise canvas
        self.frame.pack()
        self.canvas.pack()
        self.canvas.focus_set()

        # Initialise players
        self.players = []
        self.spawnPlayer()

        # refresh
        self.refreshAgain = True
        self.refresh()

    def refresh(self):
        # player logic
        for player in self.players:
            bottom = int(SIZE)-player.size

            # gravity:
            if player.y < bottom:
                player.fall()
            else:
                # if player is below bottom of screen: move to bottom
                difference = bottom - player.y
                self.canvas.move(player.canvasObject, 0 , difference)
                player.y += difference
            

                

        self.master.update()
        if self.refreshAgain:
            self.master.after(REFRESH_DELAY,self.refresh)


    

SIZE = "800"
GRAVITY = 0.5
JUMP_STRENGTH = -10
MOVEMENT_SPEED = 5
REFRESH_DELAY = 10

if __name__ == '__main__':
    root = tk.Tk()

    app = App(root)
    app.draw()

    root.mainloop()