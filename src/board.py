import pygame as pg
from .piece import (
    Piece,
    Bishop,
    King,
    Pawn,
    Rook,
    Queen,
    Knight
)

class Board:

    def __init__(self, display):

        # SCREEN -------
        self.screen = display
        self.W, self.H = display.get_size()

        # board pos
        self.pos = (60, 60)

        # PIECES -------
        self.pieces: list[Piece] = [
            Pawn("a7", "black"), Pawn("b7", "black"), Pawn("c7", "black"), Pawn("d7", "black"),
            Pawn("e7", "black"), Pawn("f7", "black"), Pawn("g7", "black"), Pawn("h7", "black"),
            Rook("a8", "black"), Rook("h8", "black"), Bishop("c8", "black"), Bishop("f8", "black"),
            Queen("d8", "black"), King("e8", "black"), Knight("b8", "black"), Knight("g8", "black"),
            Pawn("a2", "white"), Pawn("b2", "white"), Pawn("c2", "white"), Pawn("d2", "white"),
            Pawn("e2", "white"), Pawn("f2", "white"), Pawn("g2", "white"), Pawn("h2", "white"),
            Rook("a1", "white"), Rook("h1", "white"), Knight("b1", "white"), Knight("g1", "white"),
            Bishop("c1", "white"), Bishop("f1", "white"), King("e1", "white"), Queen("d1"," white")
        ]

        # TILES --------
        self.tile_size: int = 85
        # colors
        self.black = (118, 150, 86)
        self.white = (238, 238, 210)

        # selection
        self.selected = None

        # Temporaire, pour montrer quelle case tu selectionnes
        self.selected_surf = pg.Surface((self.tile_size, self.tile_size), pg.SRCALPHA)
        self.selected_surf.set_alpha(128)
        self.selected_surf.fill((0, 255, 0))

    def select(self, pos: tuple[int, int]):
        for piece in self.pieces:
            if piece.rect.collidepoint(pos):
                self.selected = piece.index
                return
        self.selected = None

    def update(self):

        for row in range(8):
            for col in range(8):
                if row % 2 == 0:
                    color = self.white if col % 2 == 0 else self.black
                else:
                    color = self.black if col % 2 == 0 else self.white
                pg.draw.rect(self.screen, color, [(self.pos[0]+col*self.tile_size, self.pos[1]+row*self.tile_size),
                                                  (self.tile_size, self.tile_size)])

        for piece in self.pieces:
            piece.render(self.screen, self.tile_size, self.pos)

        if self.selected is not None:
            pos = (self.pos[0]+self.selected[1]*self.tile_size, self.pos[1]+self.selected[0]*self.tile_size)
            self.screen.blit(self.selected_surf, pos)
