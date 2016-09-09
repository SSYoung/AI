#-------------------------------------------------------------------------------
# Name:        9 by 9 Sudoku Board
# Purpose:     Generate code capable of solving a partially filled sudoku board.
#
# Author:      Stefan
#
# Created:     15/11/2014
# Copyright:   (c) Stefan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#Global Constants
MAX = 9
#-------------------------------------------------------------------------------
def printSudokuBoard (matrix):
    count = 0
    for r in range(MAX):
        for c in range(MAX):
            if(count%9==0):
                print(" ")
                for x in range(45):
                    print("-",end = "")
                print(" ")
            print(matrix[r][c], " | ", end = "")
            count +=1
#-------------------------------------------------------------------------------
def recursivelySolveSudokuBoard(matrix):
    if isValidMatrix(matrix):
        print("\nSOLVED")
        return True
    else:
        r, c = coordinatesOfNextGuess(matrix)
        valGuess = 1
        validSolution = False
        while( (validSolution != True) and (valGuess<10)):
             if guessedDoesNotConflictWithMatrix(r,c,valGuess,matrix):
                matrix[r][c] = valGuess
                if(recursivelySolveSudokuBoard(matrix) == True):
                    validSolution = True
                    return True
                else:
                    matrix[r][c] = 0
             valGuess += 1
    return validSolution
#-------------------------------------------------------------------------------
def guessedDoesNotConflictWithMatrix(r,c,valGuess,matrix):
    blockNumber = getBlockNumber(r,c)
    blocks = getBlockValues(matrix)
    for cellVal in blocks[blockNumber]:
            if valGuess == cellVal:
                return False
    rowSet = [matrix[r][col] for col in range(MAX)]
    for cellVal in rowSet:
            if valGuess == cellVal:
                return False
    colSet = [matrix[row][c] for row in range(MAX)]
    for cellVal in colSet:
            if valGuess == cellVal:
                return False
    return True

#-------------------------------------------------------------------------------
def coordinatesOfNextGuess(matrix):
    for r in range(MAX):
        for c in range(MAX):
            if(matrix[r][c] == 0):
                return r,c
    return 0,0
#-------------------------------------------------------------------------------
def getBlockNumber(row,col):
        if(row < 3) and (col < 3): return 0         # 0 1 2
        if(row < 3) and (2 < col < 6): return 1     # 3 4 5
        if(row < 3) and (5 < col): return 2         # 6 7 8
        if(2 < row < 6) and (col < 3): return 3
        if(2 < row < 6) and (2 < col < 6): return 4
        if(2 < row < 6) and (5 < col): return 5
        if(5 < row) and (col < 3): return 6
        if(5 < row) and (2 < col < 6): return 7
        if(5 < row) and (5 < col): return 8
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
def isValidMatrix(matrix):
    rows = [ [],[],[], [],[],[], [],[],[],]
    cols = [ [],[],[], [],[],[], [],[],[],]
    for r in range(MAX):
        for c in range(MAX):
            rows[r].append(matrix[r][c])
            cols[c].append(matrix[r][c])

    block = getBlockValues(matrix)

    for r in rows:
        for n in range(1,MAX+1):
            if n not in r:
                return False

    for c in cols:
        for n in range(1,MAX+1):
            if n not in c:
                return False

    for b in block:
        for n in range(1,MAX+1):
            if n not in b:
                return False

    return True
#-------------------------------------------------------------------------------
def main():
    from time import clock
    start = clock()
    matrix = [[4,8,1,5,0,9,6,7,0,],
             [3,0,0,8,1,6,0,0,2,],
             [5,0,0,7,0,3,0,0,8,],
             [2,0,0,0,0,0,0,0,9,],
             [9,0,0,0,0,0,0,0,1,],
             [8,0,0,0,0,0,0,0,4,],
             [0,3,9,2,7,5,4,8,0,],
             [6,0,0,0,0,0,9,2,7,],
             [7,0,0,0,0,0,3,1,0,],]
    # matrix = [ [8,0,0,0,0,0,0,0,0],
    #            [0,0,3,6,0,0,0,0,0],
    #            [0,7,0,0,9,0,2,0,0],
    #            [0,5,0,0,0,7,0,0,0],
    #            [0,0,0,0,4,5,7,0,0],
    #            [0,0,0,1,0,0,0,3,0],
    #            [0,0,1,0,0,0,0,6,8],
    #            [0,1,0,0,9,2,0,0,5],
    #            [0,9,0,0,0,0,4,0,0], ]
    printSudokuBoard(matrix)
    if(recursivelySolveSudokuBoard(matrix)):
        printSudokuBoard(matrix)
    else:
        printSudokuBoard(matrix)
    print('   time =', round(clock()-start,1), 'seconds')

if __name__ == '__main__':
    main()
