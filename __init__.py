#Py-Chess
import sys, pygame
from classes import Color, Board
pygame.init()

SCRWIDTH, SCRHGHT, RUNNING = 1600, 800, True
BOARDWIDTH, BOARDHGTH = 800, 800
SQUARESIZE = BOARDWIDTH // 8
backgroundColor = Color(0, 0, 0, 0)

display = pygame.display.set_mode((SCRWIDTH, SCRHGHT))
board = Board(BOARDWIDTH, BOARDHGTH)
board.loadPieces(SQUARESIZE)

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        #events
    display.fill(backgroundColor.getRGB())
    board.displayBoard(display)

    board.displayPieces(display, SQUARESIZE)
    pygame.display.flip()
