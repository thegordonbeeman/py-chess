import pygame

IMAGES = {}


def rectangleToSquare(w, h):
    return ((w >= h) and (h, h)) or (w, w)


class Color:
    def __init__(self, r, g, b, a):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a
    
    def getRGB(self):
        return self.red, self.green, self.blue
    
    def getRGBA(self):
        return self.red, self.green, self.blue, self.alpha


class Board:
    def __init__(self, scrw, scrh):
        self.boardImage = pygame.image.load("res/board.png")
        self.rect = self.boardImage.get_rect()

        sqr = rectangleToSquare(scrw, scrh)
        self.board = pygame.transform.scale(self.boardImage, rectangleToSquare(scrw, scrh))
        self.rect = self.rect.move(scrw/2-sqr[0]/2, scrh/2-sqr[1]/2)

        self.tileSize = sqr[0]/8
        self.tileSet = [
            [13, 11, 12, 15, 14, 12, 11, 13],
            [10, 10, 10, 10, 10, 10, 10, 10],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [20, 20, 20, 20, 20, 20, 20, 20],
            [23, 21, 22, 25, 24, 22, 21, 23]
        ]

    def displayBoard(self, display):
        display.blit(self.board, self.rect)

    def loadPieces(self, SQUARESIZE):
        piecesList = [20, 21, 22, 23, 24, 25, 10, 11, 12, 13, 14, 15]
        for piece in piecesList:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load("res/" + str(piece) + ".png"), (SQUARESIZE, SQUARESIZE))

    def displayPieces(self, display, SQUARESIZE):
        for i in range(8):
            for j in range(8):
                piece = self.tileSet[i][j]
                print(piece)
                if piece != 0:
                    display.blit(IMAGES[piece], pygame.Rect(j * SQUARESIZE, i * SQUARESIZE, SQUARESIZE, SQUARESIZE))


class Piece:
    def __init__(self, name, id, movList, texture, team):
        self.name = name
        self.id = id #0 Pion, 1 Cavalier, 2 Fou, 3 Tour, 4 Dame, 5 Roi // 2 blanc, 1 noir
        self.movList = movList
        self.team = team

        self.image = pygame.image.load(texture)
        self.rect = self.image.get_rect()

        self.pos = x, y = 0, 0
