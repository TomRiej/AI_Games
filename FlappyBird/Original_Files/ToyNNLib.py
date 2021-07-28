import MatrixMathsLib as mml
from math import exp
from random import random

def sigmoid(x):
    return 1 / (1 + exp(-x))

class NeuralNetwork:
    def __init__(self, inputNodes, hiddenNodes, outputNodes):
        if isinstance(inputNodes, NeuralNetwork):
            a = inputNodes
            self.inputNodes = a.inputNodes
            self.hiddenNodes = a.hiddenNodes
            self.outputNodes = a.outputNodes

            # Matrix( output number, input number)
            self.weightsIH = a.weightsIH.copy()
            self.weightsHO = a.weightsHO.copy()

            self.biasH = a.biasH.copy()
            self.biasO = a.biasO.copy()
        else:
            self.inputNodes = inputNodes
            self.hiddenNodes = hiddenNodes
            self.outputNodes = outputNodes

            self.weightsIH = mml.Matrix(self.hiddenNodes, self.inputNodes)
            self.weightsHO = mml.Matrix(self.outputNodes, self.hiddenNodes)
            self.weightsIH.randomize()
            self.weightsHO.randomize()

            self.biasH = mml.Matrix(self.hiddenNodes, 1)
            self.biasO = mml.Matrix(self.outputNodes, 1)
            self.biasH.randomize()
            self.biasO.randomize()
        

    def feedForward(self, inputsArr):
        inputMatrix = mml.Matrix.fromArray(inputsArr)

        # generate hidden layer outputs
        hiddenLayerOutput = mml.Matrix.multiply(self.weightsIH, inputMatrix)
        hiddenLayerOutput.add(self.biasH)
        # activation function
        hiddenLayerOutput.mapFunc(sigmoid)

        # generate final output
        output = mml.Matrix.multiply(self.weightsHO, hiddenLayerOutput)
        output.add(self.biasO)
        output.mapFunc(sigmoid)
        
        return output.toArray()


    def mutate(self, func):
        self.weightsIH.mapFunc(func)
        self.weightsHO.mapFunc(func)
        self.biasH.mapFunc(func)
        self.biasO.mapFunc(func)

    def copy(self):
        return NeuralNetwork(self, None, None)

    def printAttributes(self):
        print("weights input -> hidden")
        self.weightsIH.printM()
        print("weights hidden -> output")
        self.weightsHO.printM()
        print("bias hidden")
        self.biasH.printM()
        print("bias output")
        self.biasO.printM()

    def strAttributes(self):
        endString = "Weights Input -> Hidden:\n"
        endString += self.weightsIH.strData()
        endString += "\nWeights Hidden -> Output:\n"
        endString += self.weightsHO.strData()
        endString += "\nBias Hidden:\n"
        endString += self.biasH.strData()
        endString += "\nBias Output:\n"
        endString += self.biasO.strData()
        return endString

# Test if its working: (Successful)
# nn = NeuralNetwork(2,1,1)

# nn.weightsIH.data[0][0] = 0.5
# nn.weightsIH.data[0][1] = -0.5

# nn.weightsHO.data[0][0] = 0.2

# nn.biasH.data[0][0] = 0.3
# nn.biasO.data[0][0] = -0.2

# nn.printAttributes()

# inputs = [0.5,0.3]
# print(nn.feedForward(inputs))

# nn = NeuralNetwork(2,2,1)
# nn.printAttributes()
# print()
# print(nn.strAttributes())




