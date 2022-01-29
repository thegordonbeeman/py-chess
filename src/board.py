import pygame as pg
from typing import Union

from .utils import pos_to_index, index_to_pos
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

        # GAME VAR -----
        self.turn = "white"  # turns to black if played
        self.targets: list = []

        # PIECES -------
        self.pieces: list[Piece] = [
            Pawn(self, "a7", "black"), Pawn(self, "b7", "black"), Pawn(self, "c7", "black"), Pawn(self, "d7", "black"),
            Pawn(self, "e7", "black"), Pawn(self, "f7", "black"), Pawn(self, "g7", "black"), Pawn(self, "h7", "black"),
            Rook(self, "a8", "black"), Rook(self, "h8", "black"), Bishop(self, "c8", "black"),
            Bishop(self, "f8", "black"), Queen(self, "d8", "black"), King(self, "e8", "black"),
            Knight(self, "b8", "black"), Knight(self, "g8", "black"), Pawn(self, "a2", "white"),
            Pawn(self, "b2", "white"), Pawn(self, "c2", "white"), Pawn(self, "d2", "white"), Pawn(self, "e2", "white"),
            Pawn(self, "f2", "white"), Pawn(self, "g2", "white"), Pawn(self, "h2", "white"), Rook(self, "a1", "white"),
            Rook(self, "h1", "white"), Knight(self, "b1", "white"), Knight(self, "g1", "white"),
            Bishop(self, "c1", "white"), Bishop(self, "f1", "white"), King(self, "e1", "white"),
            Queen(self, "d1", "white"), Pawn(self, "b3", "black")
        ]
        self.board = [[0 for _ in range(8)] for _ in range(8)]

        # TILES --------
        self.tile_size: int = 85
        # colors
        self.black = (118, 150, 86)
        self.white = (238, 238, 210)

        # selection
        self.selected = None
        self.piece_selected: Union[Piece, None] = None

        # Temporaire, pour montrer quelle case tu selectionnes
        self.selected_surf = pg.Surface((self.tile_size, self.tile_size), pg.SRCALPHA)
        self.selected_surf.set_alpha(128)
        self.selected_surf.fill((0, 255, 0))

    def get_piece(self, index: tuple[int, int]) -> Union[Piece, int]:
        return self.board[index[0]][index[1]]

    def check_pos_available(self, position: str) -> bool:
        try:
            pos_to_index(position)
        except Exception as e:
            print(e)
            return False
        return self.check_index_available(pos_to_index(position))

    def check_index_available(self, index: tuple[int, int]) -> bool:
        if index[0] > 7 or index[0] < 0 or index[1] < 0 or index[1] > 7:
            return False
        if self.board[index[0]][index[1]] != 0:
            return False
        return True

    def select(self, pos: tuple[int, int]):
        for piece in self.pieces:
            if piece.rect.collidepoint(pos) and piece.color == self.turn:
                self.selected = piece.index
                self.piece_selected = piece
                return
        self.selected = None

    def next_turn(self):
        self.selected = None
        self.piece_selected = None
        self.turn = {"white": "black", "black": "white"}[self.turn]
        self.targets = []

    def handle_clicks(self, pos: tuple[int, int]):
        if self.selected is None:
            return self.select(pos)
        else:
            if len(self.targets) != 0 and self.piece_selected is not None:
                target_rects = [pg.Rect((self.pos[0]+pos_to_index(index)[0]*self.tile_size,
                                         self.pos[1]+pos_to_index(index)[1]*self.tile_size),
                                        (self.tile_size, self.tile_size)) for index in self.targets]
                for index, rect in enumerate(target_rects):
                    if rect.collidepoint(pos):
                        self.piece_selected.move(self.targets[index])
                        return self.next_turn()
                self.selected = None
                self.piece_selected = None
            else:
                self.selected = None
                self.piece_selected = None

    def update(self):

        self.targets = []
        # update the board
        self.board = []
        all_indexes = [piece.index for piece in self.pieces]
        for r in range(8):
            row = []
            for c in range(8):
                if [r, c] in all_indexes:
                    row.append(self.pieces[all_indexes.index([r, c])])
                else:
                    row.append(0)
            self.board.append(row)

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
            pos = (self.pos[0]+self.selected[0]*self.tile_size, self.pos[1]+self.selected[1]*self.tile_size)
            self.screen.blit(self.selected_surf, pos)

            playable_indexes = self.piece_selected.generate_move_available()
            if type(playable_indexes) is list:  # temporary: remove the condition when every piece is finished
                self.targets = playable_indexes
            else:
                self.targets = []

            for target in self.targets:
                index = pos_to_index(target)
                pos = (self.pos[0]+index[0]*self.tile_size, self.pos[1]+index[1]*self.tile_size)
                self.screen.blit(self.selected_surf, pos)

        """
        Debug : show the board in the console
        for row in self.board:
            print("\t".join([str(col) for col in row]))
        print("\n")
        """
