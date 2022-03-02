from .piece import Knight, Rook, Bishop, Queen, Pawn, King


class Checker:
    
    def __init__(self, board_instance):
        self.board = board_instance
        self.color = "white"

    def check_square_pins(self, index_: tuple[int, int], color: str):
        pinned_pieces = []
        self.color = color
        directions = [[(-1, -1), (-1, 1), (1, -1), (1, 1)], [(-1, 0), (0, -1), (0, 1), (1, 0)]]
        knight_check, knight_position = self.knight_check(index_)
        pawn_check, pawn_position = self.pawn_check(index_)
        bishop_check, bishop_possible_squares, bishop_pinned_pieces = self.queen_check(index_, directions[0], [Queen, Bishop], (Knight, Rook))
        rook_check, rook_possible_squares, rook_pinned_pieces = self.queen_check(index_, directions[1], [Queen, Rook], (Knight, Bishop))
        if bishop_check:
            check = True
            possible_squares = bishop_possible_squares
        else:
            check = rook_check
            possible_squares = rook_possible_squares
        for _ in range(len(bishop_pinned_pieces)):
            pinned_pieces.append(bishop_pinned_pieces[_])
        for _ in range(len(rook_pinned_pieces)):
            pinned_pieces.append(rook_pinned_pieces[_])
        if knight_check and not check:
            possible_squares = [knight_position]
        elif knight_check and check:
            possible_squares = []
        elif pawn_check:
            possible_squares = [pawn_position]
        return (pawn_check or knight_check or check), possible_squares, pinned_pieces

    def knight_check(self, index_: tuple[int, int]):
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in knight_moves:
            index = index_[0] + move[0], index_[1] + move[1]
            if index[0] > 7 or index[0] < 0 or index[1] < 0 or index[1] > 7:
                continue
            elif not self.board.check_index_available(index):
                if self.board.get_piece(index).color != self.color:
                    if isinstance(self.board.get_piece(index), Knight):
                        return True, index
        return False, ()

    def pawn_check(self, index_: tuple[int, int]):
        pawn_moves = [(-1, -1), (1, -1)] if self.color == "white" else [(1, 1), (-1, 1)]
        for direction in pawn_moves:
            index = index_[0] + direction[0], index_[1] + direction[1]
            if index[0] > 7 or index[0] < 0 or index[1] < 0 or index[1] > 7:
                continue
            elif not self.board.check_index_available(index):
                if self.board.get_piece(index).color != self.color:
                    if isinstance(self.board.get_piece(index), Pawn):
                        return True, index
        return False, ()

    def queen_check(self, index_: tuple[int, int], directions, attacking_pieces, defending_pieces):
        check = False
        possible_squares = []
        pinned_pieces = []
        pinned_squares = []
        for direction in directions:
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
                        if type(self.board.get_piece(new_index)) in attacking_pieces:
                            check = True
                            for _ in range(1, length+1):
                                possible_squares.append((index_[0] + direction[0] * _, index_[1] + direction[1] * _))
                            break
                        else:
                            break
                    elif isinstance(self.board.get_piece(new_index), King):
                        for i in range(2, 7):
                            new_index = (index_[0] + direction[0] * i, index_[1] + direction[1] * i)
                            if new_index[0] > 7 or new_index[0] < 0 or new_index[1] < 0 or new_index[1] > 7:
                                break
                            elif not self.board.check_index_available(new_index):
                                if self.board.get_piece(new_index).color != self.color:
                                    if type(self.board.get_piece(new_index)) in attacking_pieces:
                                        check = True
                                        break
                                    else:
                                        break
                                else:
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
                                    if type(self.board.get_piece(new_index)) in attacking_pieces:
                                        piece = self.board.get_piece((index_[0] + direction[0] * length, index_[1] + direction[1] * length))
                                        if type(piece) in defending_pieces:
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
        return check, possible_squares, pinned_pieces
