from .piece import Knight, Rook, Bishop, Queen, Pawn, King
from copy import copy


class Checker:
    
    def __init__(self, board_instance):
        self.board = board_instance
        self.color = "white"

    def get_current_check(self, color):
        index = self.board.get_king(color).index
        return self.check_square(index, color)

    def check_square_pins(self, index_: tuple[int, int], color: str):
        possible_squares = []
        pinned_squares = []
        pinned_pieces = []
        knight_check = False
        rook_check = False
        bishop_check = False
        self.color = color
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in knight_moves:
            index = index_[0] + move[0], index_[1] + move[1]
            if index[0] > 7 or index[0] < 0 or index[1] < 0 or index[1] > 7:
                continue
            elif not self.board.check_index_available(index):
                if self.board.get_piece(index).color != self.color:
                    if isinstance(self.board.get_piece(index), Knight):
                        knight_check = True
        bishop_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in bishop_directions:
            length = 0
            blocked = False
            while not blocked:
                length += 1
                new_index = (index_[0] + direction[0] * length, index_[1] + direction[1] * length)
                if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                    break
                elif not self.board.check_index_available(new_index):    # If there is a piece
                    piece_length = length
                    if self.board.get_piece(new_index).color != self.color:    # If there is an ennemi piece
                        if type(self.board.get_piece(new_index)) in [Queen, Bishop]:
                            bishop_check = True
                            for _ in range(length):
                                possible_squares.append((index_[0] + direction[0] * _, index_[1] + direction[1] * _))
                        else:
                            break
                    elif isinstance(self.board.get_piece(new_index), King):
                        for i in range(2, 7):
                            new_index = (index_[0] + direction[0] * i, index_[1] + direction[1] * i)
                            if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                                break
                            elif not self.board.check_index_available(new_index):
                                if self.board.get_piece(new_index).color != self.color:
                                    if type(self.board.get_piece(new_index)) in [Queen, Bishop]:
                                        bishop_check = True
                                        break
                    else:   # If there is a friendly piece
                        for new_length in range(piece_length + 1, 8):    # We keep the loop going
                            new_index = (index_[0] + direction[0] * new_length, index_[1] + direction[1] * new_length)
                            if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                                blocked = True
                                break
                            elif not self.board.check_index_available(new_index):
                                if self.board.get_piece(new_index).color != self.color:
                                    # If there is a new ennemi piece
                                    if type(self.board.get_piece(new_index)) in [Queen, Bishop]:
                                        piece = self.board.get_piece((index_[0] + direction[0] * length, index_[1] + direction[1] * length))
                                        if type(piece) in [Knight, Rook]:
                                            pinned_pieces.append((piece.index, []))    # We pin the piece
                                        else:
                                            for _ in range(1, new_length+1):
                                                pinned_squares.append((index_[0] + direction[0] * _, index_[1] + direction[1] * _))
                                            pinned_pieces.append((piece.index, pinned_squares))
                                        blocked = True
                                        break
                                    else:
                                        blocked = True
                                        break
                                else:
                                    blocked = True
                                    break
        rook_directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for direction in rook_directions:
            length = 0
            blocked = False
            while not blocked:
                length += 1
                new_index = (index_[0] + direction[0] * length, index_[1] + direction[1] * length)
                if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                    break
                elif not self.board.check_index_available(new_index):
                    piece_length = length
                    if self.board.get_piece(new_index).color != self.color:
                        if type(self.board.get_piece(new_index)) in [Queen, Rook]:
                            rook_check = True
                            for _ in range(length):
                                possible_squares.append((index_[0] + direction[0] * _, index_[1] + direction[1] * _))
                        else:
                            break
                    elif isinstance(self.board.get_piece(new_index), King):
                        for i in range(2, 7):
                            new_index = (index_[0] + direction[0] * i, index_[1] + direction[1] * i)
                            if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                                break
                            elif not self.board.check_index_available(new_index):
                                if self.board.get_piece(new_index).color != self.color:
                                    if type(self.board.get_piece(new_index)) in [Queen, Rook]:
                                        rook_check = True
                    else:   # If there is a friendly piece
                        for new_length in range(piece_length + 1, 8):    # We keep the loop going
                            new_index = (index_[0] + direction[0] * new_length, index_[1] + direction[1] * new_length)
                            if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                                blocked = True
                                break
                            elif not self.board.check_index_available(new_index):
                                if self.board.get_piece(new_index).color != self.color:
                                    # If there is a new ennemi piece
                                    if type(self.board.get_piece(new_index)) in [Queen, Rook]:
                                        piece = self.board.get_piece((index_[0] + direction[0] * length, index_[1] + direction[1] * length))
                                        if type(piece) in [Knight, Bishop]:
                                            pinned_pieces.append((piece.index, []))
                                        else:
                                            for _ in range(1, new_length+1):
                                                pinned_squares.append(self.board.get_piece((index_[0] + direction[0] * _, index_[1] + direction[1] * _)))
                                            pinned_pieces.append((piece.index, pinned_squares))
                                        blocked = True
                                        break
                                    else:
                                        blocked = True
                                        break
                                else:
                                    blocked = True
                                    break
        pawn_moves = [(-1, -1), (1, -1)] if self.color == "white" else [(1, 1), (-1, 1)]
        for direction in pawn_moves:
            new_index = index_[0] + direction[0], index_[1] + direction[1]
            if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                continue
            elif not self.board.check_index_available(new_index):
                if self.board.get_piece(new_index).color != self.color:
                    if isinstance(self.board.get_piece(new_index), Pawn):
                        return True
        if knight_check:
            possible_squares = []
        return (knight_check or rook_check or bishop_check), possible_squares, pinned_pieces
