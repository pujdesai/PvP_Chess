import pygame

from const import *

class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    # blit method
    def update_blit(self, surface):
        # make moving piece size bigger
        self.piece.set_texture(size=128)
        texture = self.piece.texture

        # image
        img = pygame.image.load(texture)
        # rect
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        # blit
        surface.blit(img, self.piece.texture_rect)

    # other methods    

    def update_mouse(self, pos):
        # (x, y)
        self.mouseX, self.mouseY = pos 

    # save in case of invalid move
    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE # pos = (x, y) -> y
        self.initial_col = pos[0] // SQSIZE # pos = (x, y) -> x
    
    # save board coordinates directly
    def save_initial_board_coords(self, row, col):
        self.initial_row = row
        self.initial_col = col

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False