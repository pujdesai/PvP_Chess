import pygame

from const import *
from square import Square
from piece import *
from move import Move

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        self._create()
        self.last_move = None
        self.en_passant_target = None  # Square where en passant capture is possible
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # Check if this is a castling move
        if isinstance(piece, King) and abs(final.col - initial.col) == 2:
            self.castling(initial, final)
        else:
            # update move on console board
            self.squares[initial.row][initial.col].piece = None
            self.squares[final.row][final.col].piece = piece

            # En passant capture
            if (isinstance(piece, Pawn) and 
                self.en_passant_target and 
                final.row == self.en_passant_target.row and 
                final.col == self.en_passant_target.col):
                # Remove the captured pawn (which is behind the final square)
                captured_row = initial.row  # Same row as the moving pawn
                captured_col = final.col    # Same column as the final square
                self.squares[captured_row][captured_col].piece = None

            # pawn promotion
            if isinstance(piece, Pawn):
                self.check_promotion(piece, final)

        # moved
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move
        
        # Update en passant target for pawn double moves
        if isinstance(piece, Pawn) and abs(final.row - initial.row) == 2:
            # Set en passant target to the square the pawn jumped over
            self.en_passant_target = Square((initial.row + final.row) // 2, initial.col)
        else:
            self.en_passant_target = None

    def valid_move(self, piece, move):
        return move in piece.moves
    
    def in_check(self, color):
        """Check if the king of given color is in check"""
        # Find the king
        king = None
        king_row, king_col = None, None
        for row in range(ROWS):
            for col in range(COLS):
                square = self.squares[row][col]
                if square.has_piece():
                    if isinstance(square.piece, King) and square.piece.color == color:
                        king = square.piece
                        king_row, king_col = row, col
                        break
            if king:
                break
        
        if not king:
            return False
        
        # Check if any opponent piece can attack the king
        opponent_color = 'black' if color == 'white' else 'white'
        for row in range(ROWS):
            for col in range(COLS):
                square = self.squares[row][col]
                if square.has_piece() and square.piece.color == opponent_color:
                    piece = square.piece
                    # Check if this piece can attack the king directly
                    if self.can_attack_king(piece, row, col, king_row, king_col):
                        return True
        return False
    
    def can_attack_king(self, piece, piece_row, piece_col, king_row, king_col):
        """Check if a piece can attack the king without recursion"""
        if isinstance(piece, Pawn):
            # Pawns attack diagonally
            direction = -1 if piece.color == 'white' else 1
            attack_squares = [(piece_row + direction, piece_col - 1), 
                             (piece_row + direction, piece_col + 1)]
            # Check if attack squares are in range and contain the king
            for attack_row, attack_col in attack_squares:
                if (Square.in_range(attack_row, attack_col) and 
                    attack_row == king_row and attack_col == king_col):
                    return True
            return False
            
        elif isinstance(piece, Knight):
            # Knight moves
            knight_moves = [
                (piece_row - 2, piece_col + 1), (piece_row - 1, piece_col + 2),
                (piece_row + 1, piece_col + 2), (piece_row + 2, piece_col + 1),
                (piece_row + 2, piece_col - 1), (piece_row + 1, piece_col - 2),
                (piece_row - 1, piece_col - 2), (piece_row - 2, piece_col - 1)
            ]
            # Check if any knight move reaches the king
            for move_row, move_col in knight_moves:
                if (Square.in_range(move_row, move_col) and 
                    move_row == king_row and move_col == king_col):
                    return True
            return False
            
        elif isinstance(piece, Bishop):
            # Bishop moves diagonally
            return self.can_move_diagonally(piece_row, piece_col, king_row, king_col)
            
        elif isinstance(piece, Rook):
            # Rook moves horizontally/vertically
            return self.can_move_straight(piece_row, piece_col, king_row, king_col)
            
        elif isinstance(piece, Queen):
            # Queen moves both diagonally and straight
            return (self.can_move_diagonally(piece_row, piece_col, king_row, king_col) or
                    self.can_move_straight(piece_row, piece_col, king_row, king_col))
            
        elif isinstance(piece, King):
            # King moves one square in any direction
            return abs(king_row - piece_row) <= 1 and abs(king_col - piece_col) <= 1
            
        return False
    
    def can_move_diagonally(self, from_row, from_col, to_row, to_col):
        """Check if a piece can move diagonally from one square to another"""
        if abs(to_row - from_row) != abs(to_col - from_col):
            return False
            
        row_dir = 1 if to_row > from_row else -1
        col_dir = 1 if to_col > from_col else -1
        
        current_row = from_row + row_dir
        current_col = from_col + col_dir
        
        while current_row != to_row and current_col != to_col:
            if self.squares[current_row][current_col].has_piece():
                return False
            current_row += row_dir
            current_col += col_dir
            
        return True
    
    def can_move_straight(self, from_row, from_col, to_row, to_col):
        """Check if a piece can move straight from one square to another"""
        if from_row != to_row and from_col != to_col:
            return False
            
        if from_row == to_row:  # Horizontal move
            col_dir = 1 if to_col > from_col else -1
            current_col = from_col + col_dir
            while current_col != to_col:
                if self.squares[from_row][current_col].has_piece():
                    return False
                current_col += col_dir
        else:  # Vertical move
            row_dir = 1 if to_row > from_row else -1
            current_row = from_row + row_dir
            while current_row != to_row:
                if self.squares[current_row][from_col].has_piece():
                    return False
                current_row += row_dir
                
        return True
    
    def square_under_attack(self, row, col, defending_color):
        """Check if a square is under attack by the opponent"""
        attacking_color = 'black' if defending_color == 'white' else 'white'
        
        for r in range(ROWS):
            for c in range(COLS):
                square = self.squares[r][c]
                if square.has_piece() and square.piece.color == attacking_color:
                    piece = square.piece
                    if self.can_attack_king(piece, r, c, row, col):
                        return True
        return False
    
    def would_be_in_check(self, piece, move):
        """Check if a move would put or leave the king in check"""
        # Save current state
        initial = move.initial
        final = move.final
        captured_piece = self.squares[final.row][final.col].piece
        
        # Make the move temporarily
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        # Check if king is in check
        in_check = self.in_check(piece.color)
        

        
        # Restore the board
        self.squares[initial.row][initial.col].piece = piece
        self.squares[final.row][final.col].piece = captured_piece
        
        return in_check
    
    def has_valid_moves(self, color):
        """Check if the given color has any valid moves"""
        for row in range(ROWS):
            for col in range(COLS):
                square = self.squares[row][col]
                if square.has_piece() and square.piece.color == color:
                    # Calculate moves for this piece
                    self.calc_moves(square.piece, row, col)
                    if len(square.piece.moves) > 0:
                        return True
        return False
    
    def is_checkmate(self, color):
        """Check if the given color is in checkmate"""
        # First check if the king is in check
        if not self.in_check(color):
            return False
        
        # Find the king
        king = None
        king_row, king_col = None, None
        for row in range(ROWS):
            for col in range(COLS):
                square = self.squares[row][col]
                if square.has_piece():
                    if isinstance(square.piece, King) and square.piece.color == color:
                        king = square.piece
                        king_row, king_col = row, col
                        break
            if king:
                break
        
        if not king:
            return False
        
        # Check if king can escape check
        king.clear_moves()
        self.calc_moves(king, king_row, king_col)
        if len(king.moves) > 0:
            return False  # King can escape
        
        # Check if any other piece can block the check or capture the attacking piece
        for row in range(ROWS):
            for col in range(COLS):
                square = self.squares[row][col]
                if square.has_piece() and square.piece.color == color and square.piece != king:
                    square.piece.clear_moves()
                    self.calc_moves(square.piece, row, col)
                    if len(square.piece.moves) > 0:
                        return False  # Another piece can help
        
        return True  # No escape possible
    
    def is_stalemate(self, color):
        """Check if the given color is in stalemate"""
        return not self.in_check(color) and not self.has_valid_moves(color)
    

        
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        # Check if this is a castling move
        if isinstance(self.squares[initial.row][initial.col].piece, King):
            king = self.squares[initial.row][initial.col].piece
            
            # Queen-side castling (long castling)
            if final.col == 2:  # King moves to c1/c8
                # Move king
                self.squares[final.row][final.col].piece = king
                self.squares[initial.row][initial.col].piece = None
                
                # Move rook from a1/a8 to d1/d8
                rook = self.squares[initial.row][0].piece
                self.squares[initial.row][3].piece = rook
                self.squares[initial.row][0].piece = None
                
            # King-side castling (short castling)
            elif final.col == 6:  # King moves to g1/g8
                # Move king
                self.squares[final.row][final.col].piece = king
                self.squares[initial.row][initial.col].piece = None
                
                # Move rook from h1/h8 to f1/f8
                rook = self.squares[initial.row][7].piece
                self.squares[initial.row][5].piece = rook
                self.squares[initial.row][7].piece = None

    def calc_moves(self, piece, row, col):

        '''
            Calculate all the valid moves for a specific piece at a specific position
        '''

        def pawn_moves():
            # pawn steps depending on if its already moved or not
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create squares for the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create new move
                        move = Move(initial, final)
                        # check if move doesn't put king in check
                        if not self.would_be_in_check(piece, move):
                            # append new valid move
                            piece.add_move(move)
                    # another piece is blocking the pawn
                    else:
                        break
                # not in range
                else: break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    # Normal capture
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        # create squares for the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # check if move doesn't put king in check
                        if not self.would_be_in_check(piece, move):
                            # append new valid move
                            piece.add_move(move)
                    
                    # En passant capture
                    elif (self.en_passant_target and 
                          possible_move_row == self.en_passant_target.row and 
                          possible_move_col == self.en_passant_target.col):
                        # create squares for the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # check if move doesn't put king in check
                        if not self.would_be_in_check(piece, move):
                            # append new valid move
                            piece.add_move(move)
                        
        def knight_moves():
            # 8 possible moves for a knight
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create squares for the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # check if move doesn't put king in check
                        if not self.would_be_in_check(piece, move):
                            # append new valid move
                            piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares for the possible new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # check if move doesn't put king in check
                            if not self.would_be_in_check(piece, move):
                                # append new move
                                piece.add_move(move)

                        # has rival piece = add move (can capture) + break
                        if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            # check if move doesn't put king in check
                            if not self.would_be_in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            break

                        # has team piece = break
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    # not in range
                    else:
                        break

                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row - 1, col + 1), # upper right
                (row - 1, col - 1), # upper left
                (row + 1, col + 1), # lower right
                (row + 1, col - 1), # lower left
                (row - 1, col + 0), # up
                (row + 0, col + 1), # right
                (row + 1, col + 0), # down
                (row + 0, col - 1), # left
            ]

            # normal moves
            for adj in adjs:
                possible_move_row, possible_move_col = adj

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create squares for the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # check if move doesn't put king in check
                        if not self.would_be_in_check(piece, move):
                            # append new valid move
                            piece.add_move(move)

            # castling moves
            if not piece.moved and not self.in_check(piece.color):
                # queen castling (long castling)
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook) and not left_rook.moved:
                    # check if squares between king and rook are empty
                    can_castle = True
                    for c in range(1, 4):
                        if self.squares[row][c].has_piece():
                            can_castle = False
                            break
                    
                    if can_castle:
                        # Check if king and squares it passes through are not under attack
                        squares_safe = True
                        for c in range(4, 2, -1):  # Check e1->d1->c1 or e8->d8->c8
                            if self.square_under_attack(row, c, piece.color):
                                squares_safe = False
                                break
                        
                        if squares_safe:
                            # create castling move
                            initial = Square(row, col)
                            final = Square(row, 2)  # king moves to c1/c8
                            move = Move(initial, final)
                            piece.add_move(move)

                # king castling (short castling)
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook) and not right_rook.moved:
                    # check if squares between king and rook are empty
                    can_castle = True
                    for c in range(5, 7):
                        if self.squares[row][c].has_piece():
                            can_castle = False
                            break
                    
                    if can_castle:
                        # Check if king and squares it passes through are not under attack
                        squares_safe = True
                        for c in range(4, 7):  # Check e1->f1->g1 or e8->f8->g8
                            if self.square_under_attack(row, c, piece.color):
                                squares_safe = False
                                break
                        
                        if squares_safe:
                            # create castling move
                            initial = Square(row, col)
                            final = Square(row, 6)  # king moves to g1/g8
                            move = Move(initial, final)
                            piece.add_move(move)
                    
        if isinstance(piece, Pawn): 
            pawn_moves()

        elif isinstance(piece, Knight): 
            knight_moves()

        elif isinstance(piece, Bishop): 
            straightline_moves([
                (-1, 1), # upper right
                (-1, -1), # upper left
                (1, 1), # lower right
                (1, -1), # lower left
            ])

        elif isinstance(piece, Rook): 
            straightline_moves([
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1), # left
            ])

        elif isinstance(piece, Queen): 
            straightline_moves([
                (-1, 1), # upper right
                (-1, -1), # upper left
                (1, 1), # lower right
                (1, -1), # lower left
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1), # left
            ])

        elif isinstance(piece, King):
            king_moves()

    # creates squares for entire board
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    # add pieces to the game board
    def _add_pieces(self, color):
        # white pieces at bottom, black at top
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))