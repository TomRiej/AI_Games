import tkinter as tk
from random import randint

# =============== UTILITIES ===================
"""
since my player, platform and more need all these
basic attributes and methods, i created this Util
class to inherit from
"""
class Util:
    def __init__(self, canvas, x, y, size, colour):
        self.mainCanvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.draw()
    
    def draw(self):
        self.canvasObject = self.mainCanvas.create_rectangle(self.getDims(),fill=self.colour)

    def getDims(self):
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.size
        y2 = self.y + self.size
        return x1, y1, x2, y2

# =============== PLAYER =======================
class Player(Util):
    def __init__(self, canvas, x, y, size, colour):
        # inherit needed atributes
        super().__init__(canvas, x, y, size, colour)
        self.yVel = 0

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

    def checkCollisions(self):
        dims = self.getDims()
        collisions = self.mainCanvas.find_overlapping(dims[0],dims[1],dims[2],dims[3])
        if len(collisions) > 1:
            self.mainCanvas.delete(collisions[1])

# =============== COLOUR CHANGER =======================
class ColourChanger(Util):
    def __init__(self, canvas, x, y, size, colour):
        super().__init__(canvas,x, y, size, colour)
        

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
        newPlayer = Player(self.canvas, 400, 400, 50, "grey")
        self.players.append(newPlayer)

    def spawnColourChanger(self, c):
        size = 30
        x = 100*c + 50
        y = 600 #randint(0,int(SIZE)-size)
        colour = COLOURS[c] #COLOURS[randint(0,6)]
        newChanger = ColourChanger(self.canvas, x, y, size, colour)
        self.changers.append(newChanger)



    def draw(self):
        # Initialise canvas
        self.frame.pack()
        self.canvas.pack()
        self.canvas.focus_set()

        # Initialise players
        self.players = []
        self.spawnPlayer()

        # Initialise changers
        self.changers = []
        for i in range(7):
            self.spawnColourChanger(i)

        # Initialise Variables
        self.floor = int(SIZE)-self.players[0].size
        self.direction = 0
        

        # refresh
        self.refreshAgain = True
        self.refreshCount = 0
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

            #collision detection
            player.checkCollisions()
        
        # # colour logic
        # if self.refreshCount % 50 == 0:
        #     self.spawnColourChanger()
            

        self.master.update()
        if self.refreshAgain:
            self.refreshCount += 1
            self.master.after(REFRESH_DELAY,self.refresh)


    
# =============== CONSTANTS =======================

SIZE = "800"
GRAVITY = 0.5
JUMP_STRENGTH = -15
MOVEMENT_SPEED = 5
REFRESH_DELAY = 10

COLOURS = {0:"#ff0000", # Red
            1:"#ff9000", # Orange
            2:"#ffdd00", # Yellow
            3:"#00ff00", # Green
            4:"#00c3ff", # Blue
            5:"#e600ff", # Pink
            6:"#9900ff" # Purple
            }


# =============== MAIN =======================
if __name__ == '__main__':
    root = tk.Tk()

    app = App(root)
    app.draw()

    root.mainloop()