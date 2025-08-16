import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('CHESS')
        self.game = Game()

    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)
            game.show_check_indicator(screen)
            game.show_game_info(screen)

            if dragger.dragging:
                dragger.update_blit(screen)
            
            # Show game over screen if game is over
            game.show_game_over(screen)

            for event in pygame.event.get():
                
                # click piece
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Don't allow moves if game is over
                    if game.game_over:
                        continue
                        
                    dragger.update_mouse(event.pos)

                    # which row & col has been clicked?
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # Convert display coordinates to board coordinates if board is flipped
                    if game.board_flipped:
                        board_row = ROWS - 1 - clicked_row
                        board_col = COLS - 1 - clicked_col
                    else:
                        board_row = clicked_row
                        board_col = clicked_col

                    # does clicked square have a piece?
                    if board.squares[board_row][board_col].has_piece():
                        piece = board.squares[board_row][board_col].piece
                        # valid piece color
                        if piece.color == game.next_player:
                            piece.clear_moves()
                            board.calc_moves(piece, board_row, board_col)
                            # Save board coordinates, not display coordinates
                            dragger.save_initial_board_coords(board_row, board_col)
                            dragger.drag_piece(piece)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                # move piece (mouse motion)
                elif event.type == pygame.MOUSEMOTION:
                    motion_col = event.pos[0] // SQSIZE
                    motion_row = event.pos[1] // SQSIZE

                    # Convert display coordinates to board coordinates if board is flipped
                    if game.board_flipped:
                        board_motion_row = ROWS - 1 - motion_row
                        board_motion_col = COLS - 1 - motion_col
                    else:
                        board_motion_row = motion_row
                        board_motion_col = motion_col

                    # check if hover is within range
                    if Square.in_range(board_motion_row, board_motion_col):
                        game.set_hover(board_motion_row, board_motion_col)
                    else:
                        # reset hover if outside the board
                        game.hovered_square = None

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # release piece
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # Convert display coordinates to board coordinates if board is flipped
                        if game.board_flipped:
                            board_released_row = ROWS - 1 - released_row
                            board_released_col = COLS - 1 - released_col
                        else:
                            board_released_row = released_row
                            board_released_col = released_col

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(board_released_row, board_released_col)
                        move = Move(initial, final)

                        # if valid move -> move
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[board_released_row][board_released_col].has_piece()

                            board.move(dragger.piece, move)
                            # Record move in history
                            game.add_move_to_history(dragger.piece, move, captured)
                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()
                            
                    dragger.undrag_piece()

                # key press
                elif event.type == pygame.KEYDOWN:

                    # press 'T' to change themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # press 'F' to flip board
                    if event.key == pygame.K_f:
                        game.toggle_board_flip()

                    # press 'R' to restart game
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                
                # quit game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            



            pygame.display.update()


main = Main()
main.mainloop()