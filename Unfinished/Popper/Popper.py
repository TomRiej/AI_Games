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
        self.sizeX = size
        self.sizeY = size
        self.colour = colour
    
    def draw(self):
        self.canvasObject = self.mainCanvas.create_rectangle(self.getDims(),fill=self.colour)

    def getDims(self):
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.sizeX
        y2 = self.y + self.sizeY
        return x1, y1, x2, y2

# =============== PLAYER =======================
class Player(Util):
    def __init__(self, canvas, x, y, size, colour):
        # inherit needed atributes
        super().__init__(canvas, x, y, size, colour)
        self.yVel = 0
        self.draw()

    def fall(self):
        self.mainCanvas.move(self.canvasObject, 0, self.yVel)
        self.y += self.yVel
        self.yVel += GRAVITY
    
    def moveHorizontal(self, direction):
        step = direction*MOVEMENT_SPEED
        if self.x  + self.sizeX + step < int(SIZE) and self.x + step > 0:
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
            return collisions[0:]

    def changeColour(self, colour):
        self.mainCanvas.itemconfig(self.canvasObject, fill=colour)

    def FindClosestFloor(self, platforms):
        midpointX = self.x + (self.sizeX//2)
        midpointY = self.y + (self.sizeY//2)
        viableFloors = []
        for platform in platforms:
            if midpointX >= platform.x and midpointX <= platform.x + platform.sizeX:
                if platform.y - midpointY >= 0:
                    viableFloors.append(platform.y)
        if len(viableFloors) > 0:
            return min(viableFloors)
        else:
            return None


# =============== COLOUR CHANGER =======================
class ColourChanger(Util):
    def __init__(self, canvas, x, y, size, colour):
        super().__init__(canvas,x, y, size, colour)
        self.draw()
        

# =============== PLATFORM =======================
class Platform(Util):
    def __init__(self, canvas, x, y, sizeX, sizeY, colour):
        super().__init__(canvas, x, y, sizeX, colour)
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.draw()


# =============== MAIN APP =======================
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Popper")
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
        elif event.char == "w":
            if self.player.y == self.floor:
                self.player.jump()


    def spawnPlayer(self):
        newPlayer = Player(self.canvas, 400, 400, 50, "grey")
        self.player = newPlayer

    def spawnColourChanger(self, c):
        size = 30
        x = 100*c + 50
        y = 600 #randint(0,int(SIZE)-size)
        colour = COLOURS[c] #COLOURS[randint(0,6)]
        newChanger = ColourChanger(self.canvas, x, y, size, colour)
        self.changers.append(newChanger)

    def spawnPlatform(self, x, y, sizeX, sizeY, colour):
        newPlatform = Platform(self.canvas, x, y, sizeX, sizeY, colour)
        self.platforms.append(newPlatform)

    def makeRdmPlatform(self):
        x = randint(0, int(SIZE))
        if self.player.y-100 > 0:
            y = randint(int(self.player.y)-100, int(self.player.y))
        else:
            y = randint(0,int(self.player.y))
        sizeX = randint(50,200)
        sizeY = 20
        colour = COLOURS[randint(0,6)]
        self.spawnPlatform(x, y, sizeX, sizeY, colour)


    def draw(self):
        # Initialise canvas
        self.frame.pack()
        self.canvas.pack()
        self.canvas.focus_set()

        # Initialise players
        self.spawnPlayer()

        # Initialise changers
        self.changers = []
        for i in range(0,7):
            self.spawnColourChanger(i)

        # Initialise Platforms
        self.platforms = []

        # Initialise Variables
        self.floor = int(SIZE)-self.player.sizeY
        self.direction = 0
        

        # refresh
        self.refreshAgain = True
        self.refreshCount = 0
        self.refresh()

    def refresh(self):
        # player logic
        
        # Find Floor below player
        floor = self.player.FindClosestFloor(self.platforms)
        if floor != None:
            self.floor = floor - self.player.sizeY
                
        else:
            self.floor = int(SIZE)-self.player.sizeY
            
        # gravity:
        if self.player.y < self.floor:
            self.player.fall()
        else:
            # if player is below bottom of screen: move to bottom
            difference = self.floor - self.player.y
            self.canvas.move(self.player.canvasObject, 0 , difference)
            self.player.y += difference

        # Horrizontal movement
        self.player.moveHorizontal(self.direction)

        #collision detection
        collisions = self.player.checkCollisions()
        if collisions != None:
            for changer in self.changers:
                if changer.canvasObject in collisions:
                    self.player.changeColour(changer.colour)
        
        # Platform creation
        # if self.refreshCount % 50 == 0:
        #     self.makeRdmPlatform()
            

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