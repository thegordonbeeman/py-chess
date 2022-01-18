#Py-Chess
import sys, pygame
from classes import Color, Board
pygame.init()

SCRWIDTH, SCRHGHT, RUNNING = 1600, 900, True
backgroundColor = Color(0, 0, 0, 0)

display = pygame.display.set_mode((SCRWIDTH, SCRHGHT))
board = Board(SCRWIDTH, SCRHGHT)

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        #events
    
    display.fill(backgroundColor.getRGB())
    board.display(display)
    pygame.display.flip()