#Py-Chess
import sys, pygame, numpy
from classes import Color, Board
pygame.init()

SCRWIDTH, SCRHGHT, RUNNING = 1600, 800, True
BOARDWIDTH, BOARDHGTH = 800, 800
SQUARESIZE = BOARDWIDTH // 8
backgroundColor = Color(0, 0, 0, 0)

display = pygame.display.set_mode((SCRWIDTH, SCRHGHT))
board = Board(BOARDWIDTH, BOARDHGTH)
board.loadPieces(SQUARESIZE)

columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
rows = ['1', '2', '3', '4', '5', '6', '7', '8']
piece = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king', 'none']


def numberToColor(x):
    if x // 10 == 2:
        return True
    return False


def locationToCoordinates(x):
    return x[0] // SQUARESIZE, x[1] // SQUARESIZE


def inputToBoardCoordinates(x):
    if 0 <= x[0] <= 7 and 0 <= x[1] <= 7:
        return columns[x[0]] + rows[x[1]]


def numberToPiece(x):
    return piece[x % 10-1]


def direction(x, y):
    return numpy.sign(y[0] - x[0]), numpy.sign(y[1] - x[1])


def steps(x, y, d):       #distance entre deux points
    x0 = x[0]
    x1 = x[1]
    s = 0
    while (x0, x1) != y:
        x0 += d[0]
        x1 += d[1]
        s += 1
        if s > 7:
            return False
    return s


def validMove(start, color, direction, step, piece, endSquare):
    if piece == 'pawn':
        if pawn(start, color, direction, step, piece, endSquare):
            return True
    return False


def pawn(start, color, direction, step, piece, endSquare):
    start0, start1 = start[0], start[1]
    pawnDirection = {'N': (0, 1)}
    for l in range(1, step):
        start0 += direction[0]*l
        start1 += direction[1]*l
        if board.occupiedSquare(start1, start0, color):

            return False
    if endSquare == (start1, start0):
        return True
    return True


def makeMove(start, end, piece):
    board.tileSet[7-start[1]][start[0]] = 0
    board.tileSet[7-end[1]][end[0]] = piece

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        #events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (row, column) = locationToCoordinates(pygame.mouse.get_pos())
            pieceSelected = board.tileSet[column][row]
            startSquare = (row, 7-column)
        elif event.type == pygame.MOUSEBUTTONUP:
            (row, column) = locationToCoordinates(pygame.mouse.get_pos())
            endSquare = (row, 7-column)
            if validMove(startSquare, numberToColor(pieceSelected), direction(startSquare, endSquare),
                         steps(startSquare, endSquare, direction(startSquare, endSquare)), numberToPiece(pieceSelected),
                         endSquare):
                makeMove(startSquare, endSquare, pieceSelected)


    display.fill(backgroundColor.getRGB())
    board.displayBoard(display)

    board.displayPieces(display, SQUARESIZE)
    pygame.display.flip()