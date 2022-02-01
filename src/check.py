from .piece import Knight, Rook, Bishop, Queen, Pawn
from copy import copy


class Checker:
    
    def __init__(self, board_instance):
        self.board = board_instance
        self.color = "white"

    def get_current_check(self, color):
        index = self.board.get_king(color).index
        return self.check_square(index, color)

    def check_square(self, index_: tuple[int, int], color: str) -> bool:
        self.color = color

        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in knight_moves:
            index = index_[0] + move[0], index_[1] + move[1]
            if index[0] > 7 or index[0] < 0 or index[1] < 0 or index[1] > 7:
                continue
            elif not self.board.check_index_available(index):
                if self.board.get_piece(index).color != self.color:
                    if isinstance(self.board.get_piece(index), Knight):
                        return True
        bishop_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in bishop_directions:
            for length in range(1, 8):
                new_index = (index_[0] + direction[0] * length, index_[1] + direction[1] * length)
                if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                    break
                elif not self.board.check_index_available(new_index):
                    if self.board.get_piece(new_index).color != self.color:
                        if type(self.board.get_piece(new_index)) in [Queen, Bishop]:
                            return True
                        else:
                            break
                    else:
                        break
        rook_directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for direction in rook_directions:
            for length in range(1, 8):
                new_index = (index_[0] + direction[0] * length, index_[1] + direction[1] * length)
                if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                    break
                elif not self.board.check_index_available(new_index):
                    if self.board.get_piece(new_index).color != self.color:
                        if type(self.board.get_piece(new_index)) in [Queen, Rook]:
                            return True
                        else:
                            break
                    else:
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

        return False
