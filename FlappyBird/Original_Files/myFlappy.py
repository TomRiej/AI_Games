# Tom Rietens
# 12.12.2020
# actually WORKING
# Flappy bird AI
# takes approx 20 games to see a bird get quite far
# takes approx 40 gens to master



import tkinter as tk
from random import randint, random, gauss
import ToyNNLib as tnnl # self coded library

class Bird:
    def __init__(self, strength, brain=None):
        self.x = 150
        self.y = randint(100,400)
        self.radius = 20
        self.jumpStrength = strength
        self.velocity = 0

        self.score = 0
        self.fitness = 0

        if isinstance(brain, tnnl.NeuralNetwork):
            self.brain = brain.copy()
        else:
            self.brain = tnnl.NeuralNetwork(5,8,2)

    def copy(self):
        return Bird(self.jumpStrength, self.brain)

    def brainMutate(self):
        self.brain.mutate(Bird.mutate)

    @ staticmethod
    def mutate(x):
        if random() < 0.1:
            offset = gauss(0,0.5) * 0.5
            newx = x + offset
            return newx
        else:
            return x

    def getBirdDims(self):
        x0 = self.x - self.radius
        y0 = self.y - self.radius
        x1 = self.x + self.radius
        y1 = self.y + self.radius
        return x0,y0,x1,y1

    def checkCollision(self, points):
        # ceiling & floor collision
        if self.y < 0 or self.y > 800:
            return True

        # using pythag to test if distace to points < radius, cuz then they have collided
        radiusSquared = self.radius**2 # checking agains r squared as squareroot is tough on processing
        for point in points:
            deltaX = abs(point[0] - self.x)
            deltaY = abs(point[1] - self.y)
            magnitudeSquared = (deltaX**2) + (deltaY**2)
            if magnitudeSquared < radiusSquared:
                return True # they are colliding
            if self.x + self.radius > points[0][0]:
                if self.y < points[0][1] or self.y > points[3][1]:
                    return True

        return False

    @staticmethod
    def normalise(x):
        return x / 800

    def think(self, pipeInputs):
        normalisedY = Bird.normalise(self.y)
        normalisedVel = self.velocity / 10
        # print("y: ", self.y, normalisedY)
        # print("vel: ", self.velocity, normalisedVel)
        # print("pipe top:", pipeInputs[0], Bird.normalise(pipeInputs[0]))
        # print("pipe bot:", pipeInputs[1], Bird.normalise(pipeInputs[1]))
        # print("pipe x:", pipeInputs[2], Bird.normalise(pipeInputs[2]))
        inputs = [normalisedY, normalisedVel]
        for i in pipeInputs:
            n = Bird.normalise(i)
            inputs.append(n)
        
        output = self.brain.feedForward(inputs)
        if output[0] > output[1]:
            self.jump()

    def jump(self):
        self.velocity = 0
        self.velocity += self.jumpStrength

# ============================== Pipe ==================================


class Pipe:
    def __init__(self, pipeGap):
        self.x = 800
        self.width = 60
        self.gap = pipeGap
        self.gapStartY = randint(100,600)
        
    def getTopRect(self):
        x0 = self.x
        y0 = 0
        x1 = self.x + self.width
        y1 = self.gapStartY
        return x0,y0,x1,y1

    def getBotRect(self):
        x0 = self.x
        y0 = self.gapStartY + self.gap
        x1 = self.x + self.width
        y1 = 800
        return x0,y0,x1,y1

    def getCollisionPoints(self):
        points = []
        
        x0 = self.x
        x1 = self.x + (self.width//2)
        x2 = self.x + self.width

        # Top rect
        y = self.gapStartY
        points.append([x0,y])
        points.append([x1,y])
        points.append([x2,y])
        # Bottom rect
        y = self.gapStartY + self.gap
        points.append([x0,y])
        points.append([x1,y])
        points.append([x2,y])

        return points

    def getPipeInputs(self):
        top = self.gapStartY
        bot = self.gapStartY + self.gap
        return [top, bot, self.x]
        
# ================================= Flappy =======================================


class Flappy:
    def __init__(self, master, popSize, gravity, refreshDelay, jumpStrength, pipeGap, pipeVelocity, spawnRate):
        # Initialising basic Tkinter Configurations
        self.master = master
        self.master.title("Flappy Bird")
        self.master.geometry("800x800")
        self.refreshDelay = refreshDelay

        # Initialising Tkinter Variables
        self.frame = tk.Frame(self.master, width=800, height=800)
        self.canvas = tk.Canvas(self.frame, width=800, height=800, bg="lightblue")
        self.canvas.bind("<space>", self.onSpace)
        

        # Initialising pythonic constants
        self.popSize = popSize
        self.gravity = gravity
        self.jumpStrength = jumpStrength
        self.pipeSpawnRate = spawnRate
        self.pipeGap = pipeGap
        self.pipeVelocity = pipeVelocity
        self.allTimeHighest = 0

    def getHScore(self):
        highest = 0
        for bird in self.allBirds:
            if bird.score > highest:
                highest = bird.score
        return highest

    def onSpace(self, event):
        # if self.refreshAgain:
        #     for i in range(len(self.birds)):
        #         self.birds[i].velocity = 0
        #         self.birds[i].velocity += self.jumpStrength 
        # else:
        print("space pressed")
        # self.newgame(False)

# ========================== Game Logic =========================================

    def spawnPipe(self):
        newPipe = Pipe(self.pipeGap)
        self.pipes.append(newPipe)
        topPipe = self.canvas.create_rectangle(newPipe.getTopRect(), fill="lightgreen")
        botPipe = self.canvas.create_rectangle(newPipe.getBotRect(), fill="lightgreen")
        self.canvasPipes.append([topPipe,botPipe])

    def spawnBirds(self):
        # Init and render Bird Population
        for i in range(self.popSize):
            newBird = Bird(self.jumpStrength)
            self.allBirds.append(newBird)
            self.activeBirds.append(newBird)
            canvBird = self.canvas.create_oval(newBird.getBirdDims(), fill="yellow")
            self.canvasBirds.append(canvBird) 

    def findClosestPipeIndex(self):
        if (self.pipes[0].x + self.pipes[0].width) > (self.allBirds[0].x - self.allBirds[0].radius):  # check if Bird.x works
            return 0
        else:
            return 1

# ============================= genetic algorithm stuff ==============================
    def makeNextGen(self):
        self.calcFitnesses()
        self.pickedBirds = self.generate(self.allBirds)
        self.allBirds = []
        self.activeBirds = []
        for i in self.pickedBirds:
            self.allBirds.append(i)
            self.activeBirds.append(i)

    @ staticmethod
    def generate(oldBirds):
        newBirds = []
        for i in range(len(oldBirds)):
            bird = Flappy.pickOne(oldBirds)
            newBirds.append(bird)
        return newBirds

    @ staticmethod
    def pickOne(birds):
        # pick a bird based off fitness score
        index = 0
        r = random()
        
        while (r > 0):
            r -= birds[index].fitness
            index += 1
            # if index + 1 == len(birds):   Remove this
            #     index = 0
            # else:
            #     index += 1

        index -= 1
        # bird.copy() includes a mutation
        new = birds[index].copy()
        new.brainMutate()
        return new
        
    def calcFitnesses(self):
        # calc fitness: val 0-1 which all add up to 1
        sumScores = 0
        for bird in self.allBirds:
            bird.score = bird.score**2   
            sumScores += bird.score
        for bird in self.allBirds:
            bird.fitness = bird.score / sumScores
            
    def findBestBird(self):
        bestScore = 0
        index = 0
        for i in range(len(self.allBirds)):
            if self.allBirds[i].score > bestScore:
                bestScore = self.allBirds[i].score
                index = i
        return self.allBirds[index]

    @ staticmethod
    def writeToFile(bestBird):
        fileHandle = open("Best Brain.txt", "w")
        fileHandle.write("Best Bird Storage:\n")
        fileHandle.write("Score: "+str(bestBird.score)+"\n\n")
        fileHandle.write("Best Bird's Brain values:\n")
        fileHandle.write(bestBird.brain.strAttributes())
        fileHandle.close()


# ============================= Game stuff ===========================================
    def draw(self):
        # Initialise canvas
        self.frame.pack()
        self.canvas.pack()
        self.canvas.focus_set()
        self.generationCounter = 0
        self.bestScore = 0
        self.newgame(True)
        
        

    
    def newgame(self, initBirds):
        self.generationCounter += 1

        self.canvas.delete("all")

        self.scoreText = self.canvas.create_text(80,20, text=("best: "+ str(self.bestScore)), font="Verdana 20")
        self.genText = self.canvas.create_text(80,40, text=("Gen: "+ str(self.generationCounter)), font="Verdana 20")

        self.canvasBirds = []
        self.canvasPipes = []
        self.pipes = []
        

        # Init and render Bird Population
        if initBirds:
            self.allBirds = []
            self.activeBirds = []
            self.spawnBirds()
        else:
            for bird in self.allBirds:
                canvBird = self.canvas.create_oval(bird.getBirdDims(), fill="yellow")
                self.canvasBirds.append(canvBird) 

        # Init pipes
        self.spawnPipe()

        self.refreshCounter = 0
        self.refreshAgain = True
        self.refresh()
        

    def refresh(self):
        # game loop
        closestPipe = self.pipes[self.findClosestPipeIndex()]
        # moving birds
        for i in range(len(self.activeBirds)):
            self.activeBirds[i].score += 1
            self.activeBirds[i].velocity += self.gravity
            pipeInputs = closestPipe.getPipeInputs()    # Todo dont do this everytime
            self.activeBirds[i].think(pipeInputs)
            self.canvas.move(self.canvasBirds[i], 0, self.activeBirds[i].velocity)
            self.activeBirds[i].y += self.activeBirds[i].velocity # Todo test velocity readings

        # spawing pipes
        if self.refreshCounter >= self.pipeSpawnRate:
            self.spawnPipe()
            self.refreshCounter = 0

        # moving pipes
        for pipe in range(len(self.pipes)):
            self.canvas.move(self.canvasPipes[pipe][0], self.pipeVelocity, 0)
            self.canvas.move(self.canvasPipes[pipe][1], self.pipeVelocity, 0)
            self.pipes[pipe].x += self.pipeVelocity # todo test this

        # if pipe off screen remove it
        if self.pipes[0].x + self.pipes[0].width < 0:
            self.canvas.delete(self.canvasPipes[0])
            del self.pipes[0]
            del self.canvasPipes[0]

        # check for collisions
        points = closestPipe.getCollisionPoints()
        for i in range(len(self.activeBirds)-1,-1,-1):
            if self.activeBirds[i].checkCollision(points):
                self.canvas.delete(self.canvasBirds[i])
                del self.activeBirds[i]
                del self.canvasBirds[i]

        # if no more members in current gen, make new generation.          
        if len(self.activeBirds) == 0:
            self.refreshAgain = False
            self.bestScore = self.getHScore()
            if self.bestScore > self.allTimeHighest:
                self.allTimeHighest = self.bestScore
                bestBird = self.findBestBird()
                Flappy.writeToFile(bestBird)
            self.makeNextGen()
            
        self.master.update()
        if self.refreshAgain:
            self.refreshCounter += 1
            self.master.after(self.refreshDelay,self.refresh)
        else:
            self.newgame(False)
            


POPULATION_SIZE = 500
GRAVITY = 0.5  # easy: 0.5, hard: 0.7
JUMP_STRENGTH = -10
PIPE_GAP = 200 
PIPE_VELOCITY = -5 # easy: -5, hard: -8
PIPE_SPAWN_RATE = 85

REFRESH_DELAY = 10

if __name__ == "__main__":
    # b = Bird(10)
    # b.brain.printAttributes()
     
    # print("c")
    # c = b.copy()
    # c.brain.printAttributes()


    root = tk.Tk()

    app = Flappy(root, POPULATION_SIZE, GRAVITY, REFRESH_DELAY, JUMP_STRENGTH, PIPE_GAP, PIPE_VELOCITY, PIPE_SPAWN_RATE)
    app.draw()
    

    root.mainloop()

