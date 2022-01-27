import pygame as pg
from typing import Union
from .utils import pos_to_index, load_img, smoothscale_sq


class Piece:

    def __init__(self, name: str, position: Union[tuple[int, int], str], img: pg.Surface):
        self.name = name  # name : eg. bishop, rook, queen...

        self.position = position
        self.index = pos_to_index(self.position)

        self.image = img
        self.scaled_img = img
        self.tile_size = 0
        self.rect = self.image.get_rect()

    def generate_move_available(self):
        pass

    def move(self, new_position: str):
        # need to test if the position is available before calling this function
        self.position = new_position
        self.index = pos_to_index(self.position)

    def render(self, screen: pg.Surface, tile_size: int, pos_board: tuple[int, int]):
        # indexes are reversed because index = [row, col] and board = [row[col, col, ...], row[...]...]
        if self.tile_size != tile_size:
            self.tile_size = tile_size
            self.scaled_img = smoothscale_sq(self.image, tile_size)
        self.rect = self.scaled_img.get_rect(topleft=(pos_board[0]+self.index[1]*tile_size,
                                                      pos_board[1]+self.index[0]*tile_size))
        screen.blit(self.scaled_img, self.rect)


class Bishop(Piece):

    def __init__(self, position, color):

        super(Bishop, self).__init__("Bishop",
                                     position,
                                     load_img("res/13.png") if color == "black" else load_img("res/23.png")
                                     )

    def generate_move_available(self):
        pass
        # TODO : fonction pour générer une liste de tous les moves


class Queen(Piece):

    def __init__(self, position, color):
        super(Queen, self).__init__("Queen",
                                    position,
                                    load_img("res/15.png") if color == "black" else load_img("res/25.png")
                                    )

    def generate_move_available(self):
        pass
        # TODO : fonction pour générer une liste de tous les moves


class King(Piece):

    def __init__(self, position, color):
        super(King, self).__init__("King",
                                   position,
                                   load_img("res/16.png") if color == "black" else load_img("res/26.png")
                                   )

    def generate_move_available(self):
        pass
        # TODO : fonction pour générer une liste de tous les moves


class Knight(Piece):

    def __init__(self, position, color):
        super(Knight, self).__init__("Knight",
                                   position,
                                   load_img("res/12.png") if color == "black" else load_img("res/22.png")
                                   )

    def generate_move_available(self):
        pass
        # TODO : fonction pour générer une liste de tous les moves


class Pawn(Piece):

    def __init__(self, position, color):
        super(Pawn, self).__init__("King",
                                   position,
                                   load_img("res/11.png") if color == "black" else load_img("res/21.png")
                                   )

    def generate_move_available(self):
        pass
        # TODO : fonction pour générer une liste de tous les moves


class Rook(Piece):

    def __init__(self, position, color):
        super(Rook, self).__init__("Rook",
                                   position,
                                   load_img("res/11.png") if color == "black" else load_img("res/21.png")
                                   )

    def generate_move_available(self):
        pass
        # TODO : fonction pour générer une liste de tous les moves
