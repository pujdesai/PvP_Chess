import pygame

from const import *
from board import Board
from square import Square
from dragger import Dragger
from config import Config
from piece import King, Queen, Rook, Bishop, Knight, Pawn

class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_square = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
        self.game_over = False
        self.winner = None
        self.move_history = []
        self.move_count = 1

    # Show board methods (blit methods)

    def show_bg(self, surface):
        theme = self.config.theme
        board_flipped = self.next_player == 'black'

        for row in range(ROWS):
            for col in range(COLS):
                # Calculate display coordinates (flipped if black's turn)
                if board_flipped:
                    display_row = ROWS - 1 - row
                    display_col = COLS - 1 - col
                else:
                    display_row = row
                    display_col = col
                
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (display_col * SQSIZE, display_row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    lbl_pos = (5, 5 + display_row * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (display_col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        board_flipped = self.next_player == 'black'
        
        for row in range(ROWS):
            for col in range(COLS):
                # check if piece belongs on square
                if self.board.squares[row][col].has_piece():
                    # gets piece at that position and stores in a variable
                    piece = self.board.squares[row][col].piece

                    # show all pieces except piece being dragged
                    if piece is not self.dragger.piece:
                        # keeps piece at size 80 
                        piece.set_texture(size=80)
                        # stores the image of that piece in a variable
                        img = pygame.image.load(piece.texture)
                        
                        # Calculate display coordinates (flipped if black's turn)
                        if board_flipped:
                            display_row = ROWS - 1 - row
                            display_col = COLS - 1 - col
                        else:
                            display_row = row
                            display_col = col
                        
                        img_center = display_col * SQSIZE + SQSIZE // 2, display_row * SQSIZE + SQSIZE // 2
                        # centers the piece
                        piece.texture_rect = img.get_rect(center=img_center)
                        # tells pygame to display centered image
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme
        board_flipped = self.next_player == 'black'

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop through all valid moves
            for move in piece.moves:
                # Calculate display coordinates (flipped if black's turn)
                if board_flipped:
                    display_row = ROWS - 1 - move.final.row
                    display_col = COLS - 1 - move.final.col
                else:
                    display_row = move.final.row
                    display_col = move.final.col
                
                # color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (display_col * SQSIZE, display_row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme
        board_flipped = self.next_player == 'black'

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # Calculate display coordinates (flipped if black's turn)
                if board_flipped:
                    display_row = ROWS - 1 - pos.row
                    display_col = COLS - 1 - pos.col
                else:
                    display_row = pos.row
                    display_col = pos.col
                
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (display_col * SQSIZE, display_row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_square:
            board_flipped = self.next_player == 'black'
            
            # Calculate display coordinates (flipped if black's turn)
            if board_flipped:
                display_row = ROWS - 1 - self.hovered_square.row
                display_col = COLS - 1 - self.hovered_square.col
            else:
                display_row = self.hovered_square.row
                display_col = self.hovered_square.col
            
            # color
            color = (180, 180, 180)
            # rect
            rect = (display_col * SQSIZE, display_row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)
    
    def show_check_indicator(self, surface):
        """Show red border around king if in check"""
        if not self.game_over:
            board_flipped = self.next_player == 'black'
            
            # Check if current player is in check
            if self.board.in_check(self.next_player):
                # Find the king
                for row in range(ROWS):
                    for col in range(COLS):
                        square = self.board.squares[row][col]
                        if (square.has_piece() and 
                            isinstance(square.piece, King) and 
                            square.piece.color == self.next_player):
                            # Calculate display coordinates (flipped if black's turn)
                            if board_flipped:
                                display_row = ROWS - 1 - row
                                display_col = COLS - 1 - col
                            else:
                                display_row = row
                                display_col = col
                            
                            # Draw red border around king
                            color = (255, 0, 0)  # Red
                            rect = (display_col * SQSIZE, display_row * SQSIZE, SQSIZE, SQSIZE)
                            pygame.draw.rect(surface, color, rect, width=3)
                            return

    # other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        
        # Increment move count after black's move
        if self.next_player == 'white':
            self.move_count += 1
        
        # Check for game over conditions
        opponent = 'white' if self.next_player == 'black' else 'black'
        
        if self.board.is_checkmate(opponent):
            self.game_over = True
            self.winner = self.next_player
        elif self.board.is_stalemate(opponent):
            self.game_over = True
            self.winner = 'draw'
    
    def add_move_to_history(self, piece, move, captured=False):
        """Add a move to the move history with algebraic notation"""
        # Basic algebraic notation
        piece_symbol = self.get_piece_symbol(piece)
        from_square = Square.get_alphacol(move.initial.col) + str(8 - move.initial.row)
        to_square = Square.get_alphacol(move.final.col) + str(8 - move.final.row)
        
        notation = piece_symbol + from_square + to_square
        if captured:
            notation = piece_symbol + 'x' + to_square
        
        # Special cases
        if isinstance(piece, King) and abs(move.final.col - move.initial.col) == 2:
            notation = 'O-O' if move.final.col == 6 else 'O-O-O'  # Castling
        
        self.move_history.append(notation)
    
    def get_piece_symbol(self, piece):
        """Get the algebraic notation symbol for a piece"""
        if isinstance(piece, King):
            return 'K'
        elif isinstance(piece, Queen):
            return 'Q'
        elif isinstance(piece, Rook):
            return 'R'
        elif isinstance(piece, Bishop):
            return 'B'
        elif isinstance(piece, Knight):
            return 'N'
        elif isinstance(piece, Pawn):
            return ''  # Pawns don't get a symbol
        return ''

    def set_hover(self, row, col):
        if Square.in_range(row, col):
            self.hovered_square = self.board.squares[row][col]
        else:
            self.hovered_square = None

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()
    
    def show_game_over(self, surface):
        """Display game over message"""
        if self.game_over:
            # Create semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            
            # Game over text
            if self.winner == 'draw':
                text = "STALEMATE!"
                color = (255, 255, 0)  # Yellow
            else:
                text = f"{self.winner.upper()} WINS!"
                color = (255, 255, 255)  # White
            
            font = pygame.font.SysFont('monospace', 48, bold=True)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
            surface.blit(text_surface, text_rect)
            
            # Instructions
            font_small = pygame.font.SysFont('monospace', 24, bold=True)
            instruction_text = "Press 'R' to restart"
            instruction_surface = font_small.render(instruction_text, True, (200, 200, 200))
            instruction_rect = instruction_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
            surface.blit(instruction_surface, instruction_rect)
    
    def show_game_info(self, surface):
        """Display nothing - clean interface"""
        pass
