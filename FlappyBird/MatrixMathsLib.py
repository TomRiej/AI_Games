from random import random

class Matrix:
    def __init__(self, rows=1, cols=1):
        """constructs the basic skeleton of a matrix

        Args:
            rows (int, optional): how many rows the matrix should have. Defaults to 1.
            cols (int, optional): how many columns the matrix should have. Defaults to 1.
            Defaults to 1 just in case the user forgets to enter something.
        """
        self.rows = rows
        self.columns = cols
        self.data = []

        # initialising a matrix of 0's in the correct shape
        for row in range(self.rows):
            self.data.append([])
            for col in range(self.columns):
                self.data[row].append(0)

    def copy(self):
        m = Matrix(self.rows, self.columns)
        for row in range(self.rows):
            for col in range(self.columns):
                m.data[row][col] = self.data[row][col]
        return m


    @ staticmethod
    def fromArray(arr):
        m = Matrix(len(arr), 1)
        for i in range(len(arr)):
            m.data[i][0] = arr[i]
        return m

    def toArray(self):
        arr = []
        for row in range(self.rows):
            for col in range(self.columns):
                arr.append(self.data[row][col])
        return arr
        

    def printM(self):
        """prints the matrix out in a readable format"""
        
        for row in self.data:
            print(row)

    def strData(self):
        endString = ""
        for row in range(self.rows):
            rowString = ""
            for col in range(self.columns):
                rowString += str(self.data[row][col]) + ",    "
            endString += "row: "+str(row)+ ":    " + rowString + "\n"
        return endString

    def randomize(self):
        """randomizes every value in the matrix to a number between -1 and 1"""
        
        for row in range(self.rows):
            for col in range(self.columns):
                self.data[row][col] = random()*2 -1 # random number between -1 and 1

    def add(self, matrix):
        """Performs matrix addition on 2 matrecies of identical architecture

        Args:
            matrix (Matrix object): the matrix to be added
        """
        if self.rows != matrix.rows or self.columns != matrix.columns:
            print("both matrecies dont have same architecture")
        else:
            for row in range(self.rows):
                for col in range(self.columns):
                    self.data[row][col] += matrix.data[row][col]

    @staticmethod # static method: self should not be passed in as it isn't needed, its just usefull to have a mult method in the same namespace
    def multiply(matA, matB):
        """Performs matrix multiplication of 2 matrecies with the correct format.

        Args:
            matA (Matrix object): the original matrix
            matB (Matrix object): the matrix to multiply by (order matters: AxB != BxA for matrix mult.)

        Returns:
            Matrix object: the final outcome of the multiplication
            None: if the formats are invalid
        """
        if matA.columns != matB.rows:
            print("not valid format for multiplication")
            return None

        result = Matrix(matA.rows, matB.columns) 

        for i in range(matA.rows):               # every row matrix 1
            for k in range(matB.columns):       # every col matrix 2
                total = 0
                for j in range(matA.columns):   # every val in row
                    total += matA.data[i][j] * matB.data[j][k]
                result.data[i][k] = total
        return result

    def mapFunc(self, func):
        """performs the given function on every element in the matrix

        Args:
            func (Function identifier): identifier used to call the function with the element of the matrix
        """
        for row in range(self.rows):
            for col in range(self.columns):
                self.data[row][col] = func(self.data[row][col])

# m1 = Matrix(3,2)
# m1.randomize()
# m1.printM()
# print(m1.strData())





    


    