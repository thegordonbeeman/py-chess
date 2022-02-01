import pygame as pg
from typing import Union
from .utils import pos_to_index, load_img, smoothscale_sq, index_to_pos


class Piece:

    def __init__(self, board, name: str, position: Union[tuple[int, int], str], img: pg.Surface, color: str):
        self.name = name  # name : eg. bishop, rook, queen...
        self.color = color
        self.board = board

        self.position = position
        self.index = pos_to_index(self.position)

        self.image = img
        self.scaled_img = img
        self.tile_size = 0
        self.rect = self.image.get_rect()

    def __str__(self):
        return f"{self.name}"

    def generate_move_available(self):
        pass

    def move(self, new_position: str):
        # check for eating :
        if not self.board.check_pos_available(new_position):
            piece = self.board.get_piece(pos_to_index(new_position))
            if isinstance(piece, Piece):
                self.board.pieces.remove(piece)
        # need to test if the position is available before calling this function
        self.position = new_position
        self.index = pos_to_index(self.position)

    def render(self, screen: pg.Surface, tile_size: int, pos_board: tuple[int, int]):
        self.index = pos_to_index(self.position)
        # indexes are reversed because index = [row, col] and board = [row[col, col, ...], row[...]...]
        if self.tile_size != tile_size:
            self.tile_size = tile_size
            self.scaled_img = smoothscale_sq(self.image, tile_size)
        self.rect = self.scaled_img.get_rect(topleft=(pos_board[0] + self.index[0] * tile_size,
                                                      pos_board[1] + self.index[1] * tile_size))
        screen.blit(self.scaled_img, self.rect)


class Bishop(Piece):

    def __init__(self, board_instance, position, color):
        super(Bishop, self).__init__(board_instance, "Bishop", position,
                                     load_img("./res/13.png") if color == "black" else load_img("./res/23.png"),
                                     color)

    def generate_move_available(self):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        indexes = []
        for direction in directions:
            for length in range(1, 8):
                new_index = (self.index[0] + direction[0] * length, self.index[1] + direction[1] * length)
                if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                    break
                elif not self.board.check_index_available(new_index):
                    if self.board.get_piece(new_index).color != self.color:
                        indexes.append(new_index)
                    break
                indexes.append(new_index)
        return [index_to_pos(index) for index in indexes]


class Queen(Piece):

    def __init__(self, board_instance, position, color):
        super(Queen, self).__init__(board_instance, "Queen", position,
                                    load_img("res/15.png") if color == "black" else load_img("res/25.png"),
                                    color)

    def generate_move_available(self):
        directions = [(-1, 0), (0, -1), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        indexes = []
        for direction in directions:
            for length in range(1, 8):
                new_index = (self.index[0] + direction[0] * length, self.index[1] + direction[1] * length)
                if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                    break
                elif not self.board.check_index_available(new_index):
                    if self.board.get_piece(new_index).color != self.color:
                        indexes.append(new_index)
                    break
                indexes.append(new_index)
        return [index_to_pos(index) for index in indexes]


class King(Piece):
    def __init__(self, board_instance, position, color):
        super(King, self).__init__(board_instance, "King", position,
                                   load_img("res/16.png") if color == "black" else load_img("res/26.png"),
                                   color)

    def generate_move_available(self):
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        indexes = []
        for move in moves:
            index = self.index[0] + move[0], self.index[1] + move[1]
            if index[0] > 7 or index[0] < 0 or index[1] < 0 or index[1] > 7:
                continue
            elif not self.board.check_index_available(index):
                if self.board.get_piece(index).color != self.color and not self.board.get_check_king(
                        index, self.color):
                    indexes.append(index)
                continue
            elif self.board.get_check_king(index, self.color):
                continue
            indexes.append(index)
        return [index_to_pos(index) for index in indexes]


class Knight(Piece):

    def __init__(self, board_instance, position, color):
        super(Knight, self).__init__(board_instance, "Knight", position,
                                     load_img("res/12.png") if color == "black" else load_img("res/22.png"),
                                     color)

    def generate_move_available(self) -> list[str]:
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        indexes = []
        for move in moves:
            index = self.index[0] + move[0], self.index[1] + move[1]
            if index[0] > 7 or index[0] < 0 or index[1] < 0 or index[1] > 7:
                continue
            elif not self.board.check_index_available(index):
                if self.board.get_piece(index).color != self.color:
                    indexes.append(index)
                continue
            indexes.append(index)
        return [index_to_pos(index) for index in indexes]


class Pawn(Piece):

    def __init__(self, board_instance, position, color):
        super(Pawn, self).__init__(board_instance, "Pawn", position,
                                   load_img("res/11.png") if color == "black" else load_img("res/21.png"),
                                   color)
        self.first_move_done = False  # if the pawn hasn't moved once, then he can move "twice"

    def generate_move_available(self) -> list[str]:
        moves = (0, 1) if self.color == "black" else (0, -1)
        kills = [(1, 1), (-1, 1)] if self.color == "black" else [(1, -1), (-1, -1)]
        indexes = []

        if self.board.check_index_available(index := (self.index[0] + moves[0], self.index[1] + moves[1])):
            indexes.append(index)
            if not self.first_move_done and self.board.check_index_available(
                    index := (self.index[0], self.index[1] + 2 * moves[1])):
                indexes.append(index)

        #TODO regle en passant

        for move in kills:
            index = self.index[0] + move[0], self.index[1] + move[1]
            if self.board.check_index_available(index) or not 0 <= index[0] <= 7 or not 0 <= index[1] <= 7:
                continue
            elif type(piece_on_index := self.board.get_piece(index)) is not int:
                if piece_on_index.color != self.color:
                    indexes.append(index)
        return [index_to_pos(index) for index in indexes]


    def move(self, new_position: str):
        if not self.first_move_done:
            self.first_move_done = True
        return super().move(new_position)


class Rook(Piece):

    def __init__(self, board_instance, position, color):
        super(Rook, self).__init__(board_instance, "Rook", position,
                                   load_img("res/14.png") if color == "black" else load_img("res/24.png"),
                                   color)

    def generate_move_available(self) -> list[str]:
        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        indexes = []
        for direction in directions:
            for length in range(1, 8):
                new_index = (self.index[0] + direction[0]*length, self.index[1] + direction[1]*length)
                if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                    break
                elif not self.board.check_index_available(new_index):
                    if self.board.get_piece(new_index).color != self.color:
                        indexes.append(new_index)
                    break
                indexes.append(new_index)
        return [index_to_pos(index) for index in indexes]
