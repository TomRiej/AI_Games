import tkinter as tk
from random import randint


# =============== PLAYER =======================
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
    
    def moveHorizontal(self, direction):
        self.mainCanvas.move(self.canvasObject, direction*MOVEMENT_SPEED, 0)
        self.x += direction*MOVEMENT_SPEED

    def jump(self):
        self.yVel = 0
        self.yVel += JUMP_STRENGTH
        self.mainCanvas.move(self.canvasObject, 0, self.yVel)
        self.y += self.yVel


# =============== MAIN APP =======================
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("App Name")
        self.master.geometry(SIZE+"x"+SIZE)

        # Initialising Tkinter Variables
        self.frame = tk.Frame(self.master, width=800, height=800)
        self.canvas = tk.Canvas(self.frame, width=800, height=800, bg="LightGrey")
        self.canvas.bind("<KeyPress>", self.keyDown)


    def keyDown(self, event):
        # Handling Key inputs
        if event.char == "a":
            self.direction = -1
        elif event.char == "d":
            self.direction = 1
        elif event.char == "s":
            self.direction = 0
        if event.char == "w":
            if self.players[0].y ==self.floor:
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

        # Initialise Variables
        self.floor = int(SIZE)-self.players[0].size
        self.direction = 0

        # refresh
        self.refreshAgain = True
        self.refresh()

    def refresh(self):
        # player logic
        for player in self.players:

            # gravity:
            if player.y < self.floor:
                player.fall()
            else:
                # if player is below bottom of screen: move to bottom
                difference = self.floor - player.y
                self.canvas.move(player.canvasObject, 0 , difference)
                player.y += difference

            # Horrizontal movement
            player.moveHorizontal(self.direction)
            

        self.master.update()
        if self.refreshAgain:
            self.master.after(REFRESH_DELAY,self.refresh)


    
# =============== CONSTANTS =======================

SIZE = "800"
GRAVITY = 0.5
JUMP_STRENGTH = -10
MOVEMENT_SPEED = 5
REFRESH_DELAY = 10


# =============== MAIN =======================
if __name__ == '__main__':
    root = tk.Tk()

    app = App(root)
    app.draw()

    root.mainloop()