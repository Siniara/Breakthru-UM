import pygame
import pygame.gfxdraw
import copy
from .settings import BLUE, RED, GOLD, SILVER, SQUARE_SIZE, MARGIN


class Turn:
    def __init__(self, board, screen):
        self.current_board = board
        self.screen = screen
        self.current_player = 'S'
        self.piece_just_moved = None
        self.piece_just_moved_from = None
        self.piece_just_moved_from_px = None
        self.last_capture = False
        self._init()

    def _init(self):
        self.moves_made = 0
        self.captures = 0
        self.selected_piece = None
        self.just_moved = False
        self.valid_actions = []
        self.all_actions = {}

    # moves the selection if valid
    def select_move(self, row, col):

        if self.selected_piece:
            self._move(row, col)

        selection = self.current_board.get_tile(row, col)
        if selection not in {'-', '*'} and selection.piece_type == self.current_player:
            self.selected_piece = selection

            moves, captures = self.current_board.get_valid_actions(selection)

            if self.moves_made == 0:
                self.valid_actions = moves + captures
            else:
                self.valid_actions = moves

    def _move(self, row, col):
        destination_tile = self.current_board.get_tile(row, col)

        if destination_tile in {'-', '*'} and (row, col) in self.valid_actions and self.moves_made < 2:

            self.piece_just_moved_from = (self.selected_piece.row, self.selected_piece.col)
            self.piece_just_moved_from_px = (self.selected_piece.x, self.selected_piece.y)
            self.current_board.move(self.selected_piece, row, col)
            self.moves_made += 1
            self.piece_just_moved = self.selected_piece
            self.just_moved = True
            self.last_capture = False
            if self.selected_piece.king:
                self.current_board.king_moved += 1

        elif (row, col) in self.valid_actions and self.moves_made == 0:

            self.piece_just_moved_from = (self.selected_piece.row, self.selected_piece.col)
            self.piece_just_moved_from_px = (self.selected_piece.x, self.selected_piece.y)
            self.current_board.remove(row, col)
            self.current_board.move(self.selected_piece, row, col)
            self.captures += 1
            self.piece_just_moved = self.selected_piece
            self.just_moved = True
            self.last_capture = True
            if self.selected_piece.king:
                self.current_board.king_moved += 1

    def change_turn(self):
        if self.current_player == 'S':
            self.current_player = 'G'
        else:
            self.current_player = 'S'
        self._init()

    def change_piece(self):
        self.just_moved = False
        self.selected_piece = None
        self.valid_actions = []
        self.all_actions = {}

    def update_turn(self, game=None):

        if not self.selected_piece:
            pass

        else:
            if self.just_moved and game is not None:
                game.update_history(self.selected_piece)
                print(game.history_chess[-1])
                print(' ')

            winner = self.current_board.check_winner()

            if self.selected_piece.king:
                self.current_board.king_pos = (self.selected_piece.row, self.selected_piece.col)

                if self.just_moved:
                    self.change_turn()
                    if game is not None:
                        game.turns += 1

                elif self.moves_made >= 1:
                    self.change_piece()

            if self.captures >= 1:
                self.change_turn()
                if game is not None:
                    game.turns += 1

            elif self.moves_made >= 2:
                self.change_turn()
                if game is not None:
                    game.turns += 1

            if self.selected_piece == self.piece_just_moved:
                self.change_piece()

            return winner

    def draw_valid_actions(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, BLUE,
                               ((MARGIN + SQUARE_SIZE) * (col + 1) + MARGIN + SQUARE_SIZE // 2,
                                (MARGIN + SQUARE_SIZE) * row + MARGIN + SQUARE_SIZE // 2),
                               6)

    def draw_just_moved(self):
        start_x, start_y = self.piece_just_moved_from_px

        end_x = self.piece_just_moved.x
        end_y = self.piece_just_moved.y

        pygame.draw.line(self.screen, RED, (start_x, start_y), (end_x, end_y), 3)

    def draw_turn_color(self):
        x = 650
        y = 75

        color = SILVER if self.current_player == 'S' else GOLD

        radius = SQUARE_SIZE // 2 - 10
        pygame.draw.circle(self.screen, (0, 0, 0), (x, y), radius + 2)
        pygame.draw.circle(self.screen, color, (x, y), radius)

    def __deepcopy__(self, memodict={}):
        new_instance = Turn(copy.deepcopy(self.current_board), None)
        new_instance.__dict__.update(self.__dict__)
        return new_instance
