#-------------------------------------------------------------------------------
# Author:      Stefan
#-------------------------------------------------------------------------------
#GLOBAL CONSTANTS
MAX = 9
#-------------------------------------------------------------------------------
class cell(object):
    matrix = None
    def __init__(self,val,r,c,matrix):
        if val != 0:
            self.value = {val,}
        else:
            self.value = {1,2,3,4,5,6,7,8,9,}
        self.row = r
        self.col = c
        self.block = self.blockNumber(r,c)
        cell.matrix = matrix
    def blockNumber(self,row,col):
        if(self.row < 3) and (self.col < 3): return 0         # 0 1 2
        if(self.row < 3) and (2 < self.col < 6): return 1     # 3 4 5
        if(self.row < 3) and (5 < self.col): return 2         # 6 7 8
        if(2 < self.row < 6) and (self.col < 3): return 3
        if(2 < self.row < 6) and (2 < self.col < 6): return 4
        if(2 < self.row < 6) and (5 < self.col): return 5
        if(5 < self.row) and (self.col < 3): return 6
        if(5 < self.row) and (2 < self.col < 6): return 7
        if(5 < self.row) and (5 < self.col): return 8
#-------------------------------------------------------------------------------
def createMatrix():
    M = [ [7,9,0,0,0,0,3,0,0,],
          [0,0,0,0,0,6,9,0,0,],
          [8,0,0,0,3,0,0,7,6,],
          [0,0,0,0,0,5,0,0,2,],
          [0,0,5,4,1,8,7,0,0,],
          [4,0,0,7,0,0,0,0,0,],
          [6,1,0,0,9,0,0,0,8,],
          [0,0,2,3,0,0,0,0,0,],
          [0,0,9,0,0,0,0,5,4,],]
#    M = [ [4,8,1,5,0,9,6,7,0,],
#          [3,0,0,8,1,6,0,0,2,],
#          [5,0,0,7,0,3,0,0,8,],
#          [2,0,0,0,0,0,0,0,9,],
#          [9,0,0,0,0,0,0,0,1,],
#          [8,0,0,0,0,0,0,0,4,],
#          [0,3,9,2,7,5,4,8,0,],
#          [6,0,0,0,0,0,9,2,7,],
#          [7,0,0,0,0,0,3,1,0,],]
    matrix = []
    for r in range(MAX):
        row = []
        for c in range(MAX):
            row.append(cell(M[r][c],r,c,matrix))
        matrix.append(row)
    for r in range(MAX):
        for c in range(MAX):
            assert type(matrix[r][c].value == set)
    return matrix
#-------------------------------------------------------------------------------
def restoreValues(matrix,oldMatrix):
    for r in range(MAX):
        for c in range(MAX):
            matrix[r][c].value = oldMatrix[r][c]
    return matrix
#-------------------------------------------------------------------------------
def badMatrix(matrix):
    for r in range(MAX):
        for c in range(MAX):
            if matrix[r][c].value == set():
                return True
    return False
#-------------------------------------------------------------------------------
def deepCopy(matrix):
    matrix = []
    for r in range(MAX):
        row = []
        for c in range(MAX):
            row.append(cell(matrix[r][c],r,c,matrix))
        matrix.append(row)
    return matrix
#-------------------------------------------------------------------------------
def coordinatesOfCellWithSmallestValueSet(matrix):
    big = float('inf')
    sml = 2
    bestRow = -1
    bestCol = -1
    for r in range(MAX):
        for c in range(MAX):
            length = len(matrix[r][c].value)
            if sml <= length <= big:
                bestRow = r
                bestCol = c
                big = length
    return(bestRow,bestCol)
#-------------------------------------------------------------------------------
def recursivelySolveTheSudokuBoard(matrix):
    #Trick 1, traverse the matrix filling in all the 1 case cells
    #while changed:
    matrix = makeAllPossibleSimpleChangesToMatrix(matrix)

    if badMatrix(matrix) or solutionIsCorrect(matrix):
        return matrix
    oldMatrix = deepcopy(matrix)
    r, c = coordinatesOfCellWithSmallestValueSet(matrix)
    for guess in matrix[r][c].value:
        matrix[r][c].value = {guess}
        matrix = recursivelySolveTheSudoku(matrix)
        if solutionIsCorrect(matrix):
            return matrix
        matrix = restoreValues(matrix,oldMatrix)
    return matrix
#-------------------------------------------------------------------------------
def makeAllPossibleSimpleChangesToMatrix(matrix):
    for r in range(MAX):
        for c in range(MAX):
                if (type(matrix[r][c]) is list):
                    print ('Sim ', r, ' ', c)
                    for c in matrix[r][c]:
                        print(c.row, ' ', c.col, ' ', c.value)
                if (len(matrix[r][c].value) == 1):
                    matrix = checkTrickTwo(r,c,matrix)
                matrix = fixRowWithOneSpace(r,c,matrix)
                matrix = fixColWithOneSpace(r,c,matrix)
                matrix = fixBoxWithOneSpace(r,c,matrix)
                # if(len(matrix[r][c].value) == 1):
                #     changed = True
                #     matrix = fixRowWithOneSpace(r,c,matrix)
                #     matrix = fixColWithOneSpace(r,c,matrix)
                #     matrix = fixBoxWithOneSpace(r,c,matrix)
                #     if (type(matrix[r][c]) is list):
                #         print('list type', r, ' ', c)
                # else:
                #     matrix = checkTrickTwo(r,c,matrix)
    return matrix
#-------------------------------------------------------------------------------
def fixRowWithOneSpace(r,c,matrix):
    valSet = matrix[r][c].value
    for col in range(MAX):
        if (col != c):
            matrix[r][col].value -= valSet
    return matrix
#-------------------------------------------------------------------------------
def fixColWithOneSpace(r,c,matrix):
    valSet = matrix[r][c].value
    for row in range(MAX):
        if (row != r):
            matrix[row][c].value -= valSet
    return matrix
#-------------------------------------------------------------------------------
def fixBoxWithOneSpace(r,c,matrix):
    valSet = matrix[r][c].value
    blocks = getBlockValues(matrix)
    blockNumber = getBlockNumber(r,c)

    for cell in blocks[blockNumber]:
        if (len(cell.value) > 1):
            cell.value -= valSet
    return matrix

#-------------------------------------------------------------------------------
def checkTrickTwo(r,c,matrix):
    rowVals = set()
    colVals = set()
    boxVals = set()
    cellVals = matrix[r][c].value
    for row in range(MAX):
        if row != r:
            colVals = colVals.union(matrix[row][c].value)
    for n in cellVals:
        if {n} not in rowVals:
            matrix[r][c].value = {n}
            if (type(matrix[r][c]) is list):
                print ('Row cellVals ', r, ' ', c)

    for col in range(MAX):
        if col != c:
            rowVals = rowVals.union(matrix[r][col].value)
    for n in cellVals:
        if {n} not in colVals:
            matrix[r][c].value = {n}
            if (type(matrix[r][c]) is list):
                print ('Col cellVals ', r, ' ', c)

    block = getBlockValues(matrix)
    blockNumber = getBlockNumber(r,c)
    for cell in block[blockNumber]:
        boxVals |= matrix[cell.row][cell.col].value
    for n in cellVals:
        if {n} not in boxVals:
            matrix[r][c].value = {n}
            if (type(matrix[r][c]) is list):
                print ('Blo cellVals ', r, ' ', c)

    return matrix
#-------------------------------------------------------------------------------
def getBlockNumber(r,c):
    majorRow = (r-1) / MAX
    majorCol = (c-1) / MAX
    return int(majorCol + majorRow * MAX + 1)
#-------------------------------------------------------------------------------
def getBlockValues(matrix):
    block = [ [],[],[], [],[],[], [],[],[],]
    block[0] = [matrix[0][0], matrix[0][1], matrix[0][2],
                matrix[1][0], matrix[1][1], matrix[1][2],
                matrix[2][0], matrix[2][1], matrix[2][2],]

    block[1] = [matrix[0][3], matrix[0][4], matrix[0][5],
                matrix[1][3], matrix[1][4], matrix[1][5],
                matrix[2][3], matrix[2][4], matrix[2][5],]

    block[2] = [matrix[0][6], matrix[0][7], matrix[0][8],
                matrix[1][6], matrix[1][7], matrix[1][8],
                matrix[2][6], matrix[2][7], matrix[2][8],]

    block[3] = [matrix[3][0], matrix[3][1], matrix[3][2],
                matrix[4][0], matrix[4][1], matrix[4][2],
                matrix[5][0], matrix[5][1], matrix[5][2],]

    block[4] = [matrix[3][3], matrix[3][4], matrix[3][5],
                matrix[4][3], matrix[4][4], matrix[4][5],
                matrix[5][3], matrix[5][4], matrix[5][5],]

    block[5] = [matrix[3][6], matrix[3][7], matrix[3][8],
                matrix[4][6], matrix[4][7], matrix[4][8],
                matrix[5][6], matrix[5][7], matrix[5][8],]

    block[6] = [matrix[6][0], matrix[6][1], matrix[6][2],
                matrix[7][0], matrix[7][1], matrix[7][2],
                matrix[8][0], matrix[8][1], matrix[8][2],]

    block[7] = [matrix[6][3], matrix[6][4], matrix[6][5],
                matrix[7][3], matrix[7][4], matrix[7][5],
                matrix[8][3], matrix[8][4], matrix[8][5],]

    block[8] = [matrix[6][6], matrix[6][7], matrix[6][8],
                matrix[7][6], matrix[7][7], matrix[7][8],
                matrix[8][6], matrix[8][7], matrix[8][8],]
    return block
#-------------------------------------------------------------------------------
def solutionIsCorrect(matrix):
    rows = [ [],[],[], [],[],[], [],[],[],]
    cols = [ [],[],[], [],[],[], [],[],[],]
    for r in range(MAX):
        for c in range(MAX):
            rows[r].append(matrix[r][c].value)
            cols[c].append(matrix[r][c].value)

    block = getBlockValues(matrix)

    for r in rows:
        for n in range(1,MAX+1):
            if {n} not in r:
                return False

    for c in cols:
        for n in range(1,MAX+1):
            if {n} not in c:
                return False

    for b in block:
        for n in range(1,MAX+1):
            if {n} not in b:
                return False

    return True
#-------------------------------------------------------------------------------
def displayTheSudokuBoard(matrix):
    for r in range(MAX):
        for c in range(MAX):
            if (len(matrix[r][c].value) == 1):
                print(list(matrix[r][c].value)[0], end = " | ")
            else:
                print('x', end = " | ")
        print(" ")
    print(" ")
#-------------------------------------------------------------------------------
def main():
    matrix = createMatrix()
    matrix = recursivelySolveTheSudokuBoard(matrix)
    displayTheSudokuBoard(matrix)
    #printVerfication(matrix)

if __name__ == '__main__':
    main()
