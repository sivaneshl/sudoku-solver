import pyautogui as pag
import time
import copy

# Initialize sudoku
sudoku = [[0 for x in range(9)] for y in range(9)]

# Print Sudoku
def printSudoku():
    print('\n')
    for i in range(len(sudoku)):
        line = ''
        if i == 3 or i == 6:
            print('---------------------')
        for j in range(len(sudoku[i])):
            if j == 3 or j == 6:
                line += '| '
            line += str(sudoku[i][j]) + ' '
        print(line)


# Find the next cell to fill
def findNextCellToFill():
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                return i, j
    return -1, -1


# Validate the given cell
def isValid(i, j, e):
    # Check if e is repeated in the row
    rowOk = all([e != sudoku[i][x] for x in range(9)])
    if rowOk:
        # Check if e is repeated in the column
        colOk = all([e != sudoku[x][j] for x in range(9)])
        if colOk:
            # Check if e is repeated in the sub square
            subX, subY = 3 * (i // 3), 3 * (j // 3)
            for x in range(subX, subX + 3):
                for y in range(subY, subY + 3):
                    if sudoku[x][y] == e:
                        return False
            return True
    return False


# Solve the sudoku
def solveSudoku():
    # Check if anything is still 0
    i, j = findNextCellToFill()
    # If nothing then the sudoku is solved
    if i == -1:
        return True

    # Try out each number from 1-10 for every empty cell
    for e in range(1, 10):
        # Check if valid
        if isValid(i, j, e):
            # If valid, then assign the number to the cell
            sudoku[i][j] = e
            # Recursively solve the sudoku
            if solveSudoku():
                return True
            # If the sudoku is not solved the reset
            sudoku[i][j] = 0
    return False


def fillSudoku(e, pos):
    locx = int((pos[0] - topleftx + boxwidth/2)//boxwidth)
    locy = int((pos[1] - toplefty + boxheight/2)//boxheight)
    sudoku[locy][locx] = e


def fillCell(e, x, y):
    xcoord = topleftx + boxwidth * x
    ycoord = toplefty + boxheight * y
    pag.click(xcoord, ycoord)
    pag.press(str(e))


time.sleep(2)

topleftx = 692
toplefty = 311
bottomrightx = 959
bottomrighty = 575
boxwidth = (bottomrightx - topleftx)/8
boxheight = (bottomrighty - toplefty)/8

for i in range(1, 10):
    for pos in pag.locateAllOnScreen('images\\' + str(i) + '.png'):
        print("Filling", i)
        fillSudoku(i, pos)

printSudoku()

sudokucopy = copy.deepcopy(sudoku)
start = time.time()
solveSudoku()
end = time.time()
printSudoku()
print("solved in ", (end-start))

for x in range(9):
    for y in range(9):
        if sudokucopy[x][y] == 0:
            fillCell(sudoku[x][y], y, x)


time.sleep(5)

topleftx = 975
toplefty = 507
bottomrightx = 1307
bottomrighty = 846