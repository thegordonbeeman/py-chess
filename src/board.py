import pygame as pg
import pygame.gfxdraw
from typing import Union

from .utils import load_img, smoothscale_sq
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
            Pawn(self, (0, 1), "black"), Pawn(self, (1, 1), "black"), Pawn(self, (2, 1), "black"), Pawn(self, (3, 1), "black"),
            Pawn(self, (4, 1), "black"), Pawn(self, (5, 1), "black"), Pawn(self, (6, 1), "black"), Pawn(self, (7, 1), "black"),
            Rook(self, (0, 0), "black"), Rook(self, (7, 0), "black"), Bishop(self, (2, 0), "black"),
            Bishop(self, (5, 0), "black"), Queen(self, (3, 0), "black"),
            King(self, (4, 0), "black"),
            Knight(self, (1, 0), "black"), Knight(self, (6, 0), "black"),
            Pawn(self, (0, 6), "white"), Pawn(self, (1, 6), "white"), Pawn(self, (2, 6), "white"),
            Pawn(self, (3, 6), "white"), Pawn(self, (4, 6), "white"), Pawn(self, (5, 6), "white"),
            Pawn(self, (6, 6), "white"), Pawn(self, (7, 6), "white"),
            Rook(self, (0, 7), "white"),
            Rook(self, (7, 7), "white"), Knight(self, (1, 7), "white"), Knight(self, (6, 7), "white"),
            Bishop(self, (2, 7), "white"), Bishop(self, (5, 7), "white"),
            King(self, (4, 7), "white"),
            Queen(self, (3, 7), "white")
        ]
        self.checker = Checker(self)
        self.board = []
        all_indexes = [piece.index for piece in self.pieces]
        for r in range(8):
            row = []
            for c in range(8):
                if (r, c) in all_indexes:
                    row.append(self.pieces[all_indexes.index((r, c))])
                else:
                    row.append(0)
            self.board.append(row)

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
        self.piece_selected_index = None
        self.en_passant = None
        self.possible_squares = []
        self.in_check = False
        self.pinned_pieces = []
        self.ended_game = False

        # Temporaire, pour montrer quelle case tu selectionnes
        self.selected_surf = pg.Surface((self.tile_size, self.tile_size), pg.SRCALPHA)
        self.selected_surf.set_alpha(128)
        self.selected_surf.fill((0, 255, 0))

        # promotion
        self.selecting_pieces = False
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
        self.all_pieces_and_moves = self.generate_all_moves()

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

    def check_index_available(self, index: tuple[int, int]) -> bool:
        if index[0] > 7 or index[0] < 0 or index[1] < 0 or index[1] > 7:
            return False
        if self.board[index[0]][index[1]] != 0:
            return False
        return True

    def handle_clicks(self, pos: tuple[int, int]):
        index = ((pos[0] - 60) // 110, (pos[1] - 60) // 110)
        for piece in range(len(self.all_pieces_and_moves)):
            if index == self.all_pieces_and_moves[piece][0]:    # if we are selecting a piece
                self.piece_selected_index = piece
                self.draw_moves(self.all_pieces_and_moves[piece][1])
                self.select(index)
        if self.piece_selected is not None:
            if index in self.all_pieces_and_moves[self.piece_selected_index][1]:
                self.update_everything(index)

    def draw_moves(self, drawing_list):
        for target in drawing_list:
            pos = (self.pos[0] + target[0] * self.tile_size, self.pos[1] + target[1] * self.tile_size)
            if self.get_piece(target) == 0:
                self.screen.blit(self.go_square, pos)
            else:
                self.screen.blit(self.kill_square, pos)

    def select(self, index: (int, int)):
        for piece in self.pieces:
            if piece.index == index and piece.color == self.turn:
                self.selected = index
                self.piece_selected = piece
                return
        self.selected = None

    def update_everything(self, index):
        self.en_passant = self.check_en_passant(self.piece_selected, index)
        self.piece_selected.move(index)
        while self.selecting_promotion:
            for key, image in self.promotion_buttons[self.object_promoted.color].items():
                hitbox = self.promotion_buttons_hb[self.object_promoted.color][key]
                pg.draw.rect(self.screen, (255, 255, 255), hitbox)
                pg.draw.rect(self.screen, (0, 255, 0), hitbox, 3)
                self.screen.blit(image, hitbox)
                pg.display.update()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for key, hb in self.promotion_buttons_hb[self.object_promoted.color].items():
                            if hb.collidepoint(event.pos):
                                return self.finish_promotion(key)
                            pg.display.update()
        self.update(index)
        self.piece_selected = None
        self.next_turn()
        self.in_check, self.possible_squares, self.pinned_pieces = self.checker.check_square_pins(self.get_king(self.turn).index, self.turn)
        self.all_pieces_and_moves = self.generate_all_moves()

    def init_promotion(self, object_promoted: Piece, next_pos: (int, int)):
        self.object_promoted = object_promoted
        self.selecting_promotion = True
        index_promotion = next_pos
        position = {"Knight": pg.Vector2(0, self.tile_size), "Queen": pg.Vector2(0, self.tile_size*3),
                    "Bishop": pg.Vector2(0, self.tile_size*2), "Rook": pg.Vector2(0, self.tile_size*4)}
        for key, hitbox in self.promotion_buttons_hb[object_promoted.color].items():
            hitbox.topleft = pg.Vector2(index_promotion[0]*self.tile_size,
                                        index_promotion[1]*self.tile_size) + (
                position[key] if object_promoted.color == "white" else -position[key]) + pg.Vector2(self.pos)

    def finish_promotion(self, tag: str):
        self.pieces.append(eval(tag)(self, self.object_promoted.index, self.object_promoted.color))
        self.pieces.remove(self.object_promoted)
        self.selecting_promotion = False
        self.object_promoted = None

    def update(self, move):
        self.targets = []
        # update the board
        self.board = []
        all_indexes = [piece.index for piece in self.pieces]
        for r in range(8):
            row = []
            for c in range(8):
                if (r, c) in all_indexes:
                    row.append(self.pieces[all_indexes.index((r, c))])
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

    def check_en_passant(self, piece, index) -> Union[None, tuple[int, int]]:
        if isinstance(piece, Pawn):
            if piece.index[1] == (6 if piece.color == 'white' else 1):
                if index[1] == (4 if piece.color == 'white' else 3):
                    return index[0], index[1] + (1 if piece.color == 'white' else -1)

    def next_turn(self):
        self.selected = None
        self.piece_selected = None
        self.turn = {"white": "black", "black": "white"}[self.turn]
        self.targets = []

    def generate_all_moves(self) -> list:    # [[[piece1], [move1, move2, ...], [[piece2], [...], ...]]
        all_pieces_and_moves = []
        self.ended_game = True
        for piece in self.pieces:
            move_list = []
            if piece.color == self.turn:
                move_list = piece.generate_move_available()
                if move_list:
                    self.ended_game = False
                all_pieces_and_moves.append([piece.index, move_list])
        return all_pieces_and_moves

    """
    Debug : show the board in the console
    for row in self.board:
        print("\t".join([str(col) for col in row]))
    print("\n")
    """

