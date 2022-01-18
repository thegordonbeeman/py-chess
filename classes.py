import pygame

def rectangleToSquare(w, h):
    return ((w >= h) and (h, h)) or (w, w)

class Color():
    def __init__(self, r, g, b, a):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a
    
    def getRGB(self):
        return self.red, self.green, self.blue
    
    def getRGBA(self):
        return self.red, self.green, self.blue, self.alpha

class Board():
    def __init__(self, scrw, scrh):
        self.image = pygame.image.load("res/board.png")
        self.rect  = self.image.get_rect()

        sqr = rectangleToSquare(scrw, scrh)
        self.image = pygame.transform.scale(self.image, rectangleToSquare(scrw, scrh))
        self.rect = self.rect.move(scrw/2-sqr[0]/2, scrh/2-sqr[1]/2)

        self.tileSize = sqr[0]/8
        self.tileSet = [
            [3, 1, 2, 5, 4, 2, 1, 3],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [3, 1, 2, 4, 5, 2, 1, 3]
        ]
    
    def display(self, display):
        display.blit(self.image, self.rect)

class Piece():
    def __init__(self, name, id, movList, texture, team):
        self.name = name
        self.id = id #0 Pion, 1 Cavalier, 2 Fou, 3 Tour, 4 Dame, 5 Roi
        self.movList = movList
        self.team = team

        self.image = pygame.image.load(texture)
        self.rect  = self.image.get_rect()

        self.pos = x, y = 0, 0