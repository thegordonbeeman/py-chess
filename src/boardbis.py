import pygame as pg
import pygame.gfxdraw
from typing import Union
from copy import copy

from .utils import pos_to_index, index_to_pos
from .utils import pos_to_index, index_to_pos, load_img, smoothscale_sq
from .check import Checker
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
            Queen(self, "d1", "white")
        ]
        self.checker = Checker(self)
        self.board = [[0 for _ in range(8)] for _ in range(8)]

        # TILES --------
        self.tile_size: int = 110
        # colors
        self.black = (181, 136, 99)
        self.white = (240, 217, 181)
        self.select_color = (247, 236, 91)
        # selection square
        grey = (80, 80, 80)
        self.kill_square = pg.Surface((self.tile_size, self.tile_size), pg.SRCALPHA)
        self.kill_square.set_alpha(50)
        pg.draw.circle(self.kill_square, grey, (self.kill_square.get_width()//2,
                                                self.kill_square.get_height()//2),
                       self.kill_square.get_width()//2, width=8)
        self.go_square = pg.Surface((self.tile_size, self.tile_size), pg.SRCALPHA)
        self.go_square.set_alpha(50)
        pygame.gfxdraw.aacircle(self.go_square, self.go_square.get_width() // 2,
                                self.go_square.get_height() // 2, self.tile_size // 6, grey)
        pygame.gfxdraw.filled_circle(self.go_square, self.go_square.get_width() // 2,
                                     self.go_square.get_height() // 2, self.tile_size // 6, grey)

        # selection
        self.selected = None
        self.piece_selected: Union[Piece, None] = None
        self.en_passant = None
        self.possible_squares = []
        self.in_check = False
        self.pinned_pieces = []

        # Temporaire, pour montrer quelle case tu selectionnes
        self.selected_surf = pg.Surface((self.tile_size, self.tile_size), pg.SRCALPHA)
        self.selected_surf.set_alpha(128)
        self.selected_surf.fill((0, 255, 0))

        # promotion
        self.selecting_promotion: bool = False
        self.object_promoted: Union[None, Piece] = None
        self.promotion_buttons: dict[str, dict[str, pg.Surface]] = {
            "white": {"Knight": load_img("res/22.png", alpha=True),
                      "Bishop": load_img("res/23.png", alpha=True),
                      "Rook": load_img("res/24.png", alpha=True),
                      "Queen": load_img("res/25.png", alpha=True)},
            "black": {"Knight": load_img("res/12.png", alpha=True),
                      "Bishop": load_img("res/13.png", alpha=True),
                      "Rook": load_img("res/14.png", alpha=True),
                      "Queen": load_img("res/15.png", alpha=True)}
        }
        self.promotion_buttons_hb = {"white": {}, "black": {}}
        for color, dict_ in self.promotion_buttons.items():
            for piece, image in dict_.items():
                self.promotion_buttons[color][piece] = smoothscale_sq(image, self.tile_size)
                self.promotion_buttons_hb[color][piece] = smoothscale_sq(image, self.tile_size).get_rect()

    def get_piece(self, index: tuple[int, int]) -> Union[Piece, int]:
        return self.board[index[0]][index[1]]

    def get_king(self, color: str) -> King:
        for piece in self.pieces:
            if piece.color == color and isinstance(piece, King):
                return piece

    def get_check_king(self, index: tuple[int, int], color: str) -> bool:
        second_king = self.get_king({"white": "black", "black": "white"}[color])
        if abs(second_king.index[0]-index[0]) in [0, 1] and abs(second_king.index[1]-index[1]) in [0, 1]:
            return True
        check, self.possible_squares, _ = self.checker.check_square_pins(index, color)
        if check:
            return True
        return False

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

    def check_en_passant(self, piece, index) -> Union[None, tuple[int, int]]:
        if isinstance(piece, Pawn):
            if piece.index[1] == (6 if piece.color == 'white' else 1):
                if self.targets[index][1] == ('4' if piece.color == 'white' else '5'):
                    return piece.index[0], piece.index[1] + (-1 if piece.color == 'white' else 1)

    def handle_clicks(self, pos: tuple[int, int]):
        if not self.selecting_promotion:
            if len(self.targets) != 0 and self.piece_selected is not None:
                target_rects = [pg.Rect((self.pos[0] + pos_to_index(index)[0] * self.tile_size,
                                         self.pos[1] + pos_to_index(index)[1] * self.tile_size),
                                        (self.tile_size, self.tile_size)) for index in self.targets]
                for index, rect in enumerate(target_rects):
                    if rect.collidepoint(pos):
                        self.en_passant = self.check_en_passant(self.piece_selected, index)
                        self.piece_selected.move(self.targets[index])
                        return self.next_turn()
                self.select(pos)
            self.select(pos)
        else:
            for key, hb in self.promotion_buttons_hb[self.object_promoted.color].items():
                if hb.collidepoint(pos):
                    return self.finish_promotion(key)

    def init_promotion(self, object_promoted: Piece, next_pos: str):
        self.object_promoted = object_promoted
        self.selecting_promotion = True
        index_promotion = pos_to_index(next_pos)
        position = {"Knight": pg.Vector2(0, self.tile_size), "Queen": pg.Vector2(0, self.tile_size*3),
                    "Bishop": pg.Vector2(0, self.tile_size*2), "Rook": pg.Vector2(0, self.tile_size*4)}
        for key, hitbox in self.promotion_buttons_hb[object_promoted.color].items():
            hitbox.topleft = pg.Vector2(index_promotion[0]*self.tile_size,
                                        index_promotion[1]*self.tile_size) + (
                position[key] if object_promoted.color == "white" else -position[key]) + pg.Vector2(self.pos)

    def finish_promotion(self, tag: str):
        self.pieces.append(eval(tag)(self, self.object_promoted.position, self.object_promoted.color))
        self.pieces.remove(self.object_promoted)
        self.selecting_promotion = False
        self.object_promoted = None

    def generate_moves(self, color: str):
        moves = []
        for piece in self.pieces:
            if piece.color != color:
                continue
            moves.extend(piece.generate_move_available())
        return moves

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
                if self.selected is not None:
                    if [col, row] == list(self.selected):
                        color = self.select_color
                radius = 8
                border_bottom_left_radius = radius if [col, row] == [0, 7] else 1
                border_bottom_right_radius = radius if [col, row] == [7, 7] else 1
                border_top_left_radius = radius if [col, row] == [0, 0] else 1
                border_top_right_radius = radius if [col, row] == [7, 0] else 1
                pg.draw.rect(self.screen, color,
                             [(self.pos[0] + col * self.tile_size, self.pos[1] + row * self.tile_size),
                              (self.tile_size, self.tile_size)],
                             border_bottom_left_radius=border_bottom_left_radius,
                             border_bottom_right_radius=border_bottom_right_radius,
                             border_top_left_radius=border_top_left_radius,
                             border_top_right_radius=border_top_right_radius)

        for piece in self.pieces:
            piece.render(self.screen, self.tile_size, self.pos)

        index = (self.get_king(self.turn).index[0], self.get_king(self.turn).index[1])
        self.in_check, self.possible_squares, self.pinned_pieces = self.checker.check_square_pins(index, str(self.turn))
        print(self.in_check, self.possible_squares, self.pinned_pieces)
        # print(self.in_check, self.possible_squares, self.pinned_pieces)
        if self.selected is not None:
            pos = (self.pos[0] + self.selected[0] * self.tile_size, self.pos[1] + self.selected[1] * self.tile_size)
            self.targets = self.piece_selected.generate_move_available()

            for target in self.targets:
                index = pos_to_index(target)
                pos = (self.pos[0] + index[0] * self.tile_size, self.pos[1] + index[1] * self.tile_size)

                if self.get_piece(pos_to_index(target)) == 0:
                    self.screen.blit(self.go_square, pos)
                else:
                    self.screen.blit(self.kill_square, pos)

        if self.selecting_promotion:
            for key, image in self.promotion_buttons[self.object_promoted.color].items():
                hitbox = self.promotion_buttons_hb[self.object_promoted.color][key]
                pg.draw.rect(self.screen, (255, 255, 255), hitbox)
                pg.draw.rect(self.screen, (0, 255, 0), hitbox, 3)
                self.screen.blit(image, hitbox)