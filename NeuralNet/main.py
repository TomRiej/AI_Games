# import MatrixMathsLib as mml
import ToyNNLib as tnnl


nn = tnnl.NeuralNetwork(5,4,1)
inputs = [1,0,-5,4,2]
output = nn.feedForward(inputs)
print(output)

