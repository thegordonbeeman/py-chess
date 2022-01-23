import pygame
import numpy

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
            [14, 12, 13, 16, 15, 13, 12, 14],
            [11, 11, 11, 11, 11, 11, 11, 11],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [21, 21, 21, 21, 21, 21, 21, 21],
            [24, 22, 23, 26, 25, 23, 22, 24]
        ]
        self.whitePresence = [
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True]
        ]
        self.blackPresence = [
            [True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False]
        ]

    def occupiedSquare(self, x, y, color):  # Know if a square is occupied
        if color:
            if not self.whitePresence[x][y]:
                return True
        else:
            if not self.blackPresence[x][y]:
                return True
        return False

    def endBoard(self, square):  # Making sure pieces stay on the board
        if square[0] < 1 or square[0] > 8 or square[1] < 1 or square[1] > 8:
            return False
        return True

    def takableSquare(self, color, square):
        if color:
            if self.blackPresence[square[0]][square[1]]:
                return True
        else:
            if self.whitePresence[square[0]][square[1]]:
                return True
        return False

    def queenMove(self, color, startSquare, endSquare):
        if startSquare == endSquare:
            return False
        xDirection = numpy.sign(endSquare[0] - startSquare[0])
        yDirection = numpy.sign(endSquare[1] - startSquare[1])
        while startSquare != endSquare:
            startSquare += (xDirection, yDirection)
            if self.occupiedSquare(color, startSquare) or self.endBoard(startSquare):
                return False
            if self.takableSquare(color, startSquare):
                if startSquare == endSquare:
                    return True
                else:
                    return False
        return True

    def rookMove(self, color, startSquare, endSquare):
        if startSquare == endSquare:
            return False
        xDirection = numpy.sign(endSquare[0] - startSquare[0])
        yDirection = numpy.sign(endSquare[1] - startSquare[1])
        if xDirection != 0 and yDirection != 0:    # Only straight moves allowed
            return False
        while startSquare != endSquare:
            startSquare += (xDirection, yDirection)
            if self.occupiedSquare(color, startSquare) or self.endBoard(startSquare):
                return False
            if self.takableSquare(color, startSquare):
                if startSquare == endSquare:
                    return True
                else:
                    return False
        return True

    def bishopMove(self, color, startSquare, endSquare):
        if startSquare == endSquare:
            return False
        xDirection = numpy.sign(endSquare[0] - startSquare[0])
        yDirection = numpy.sign(endSquare[1] - startSquare[1])
        if xDirection == 0 or yDirection == 0:  # Only straight moves allowed
            return False
        while startSquare != endSquare:
            startSquare += (xDirection, yDirection)
            if self.occupiedSquare(color, startSquare) or self.endBoard(startSquare):
                return False
            if self.takableSquare(color, startSquare):
                if startSquare == endSquare:
                    return True
                else:
                    return False
        return True

    def displayBoard(self, display):
        display.blit(self.board, self.rect)

    def loadPieces(self, SQUARESIZE):
        piecesList = [21, 22, 23, 24, 25, 26, 11, 12, 13, 14, 15, 16]
        for piece in piecesList:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load("res/" + str(piece) + ".png"), (SQUARESIZE, SQUARESIZE))

    def displayPieces(self, display, SQUARESIZE):
        for i in range(8):
            for j in range(8):
                piece = self.tileSet[i][j]
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