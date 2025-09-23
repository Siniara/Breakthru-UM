import pygame
from .settings import SQUARE_SIZE, MARGIN, GOLD, SILVER, KING


class Piece:
    PADDING = 10
    OUTLINE = 2

    def __init__(self, row, col, piece_type):
        self.row = row
        self.col = col
        self.piece_type = piece_type
        self._init()

        self.x = 0
        self.y = 0
        self.calc_pos()

    def _init(self):
        if self.piece_type == 'S':
            self.color = SILVER
            self.king = False
        elif self.piece_type == 'G':
            self.color = GOLD
            self.king = False
        elif self.piece_type == 'K':
            self.color = KING
            self.piece_type = 'G'
            self.king = True

    def draw(self, screen):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(screen, self.color, (self.x, self.y), radius)

    def calc_pos(self):
        self.x = (MARGIN + SQUARE_SIZE) * (self.col + 1) + MARGIN + SQUARE_SIZE // 2
        self.y = (MARGIN + SQUARE_SIZE) * self.row + MARGIN + SQUARE_SIZE // 2

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        if self.piece_type == 'S':
            return 'S ' + str(self.row) + ',' + str(self.col)
        elif self.piece_type == 'G' and self.king:
            return 'K ' + str(self.row) + ',' + str(self.col)
        elif self.piece_type == 'G':
            return 'G ' + str(self.row) + ',' + str(self.col)
