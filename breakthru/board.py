import pygame
import random
from .grid import grid
from .piece import Piece
from .settings import WHITE, GREEN, MARGIN, SQUARE_SIZE


def draw_margins(screen, margin_down, margin_side):
    arialfont = pygame.font.SysFont('arial', 24)
    for i in range(len(margin_down)):
        down = arialfont.render('{}'.format(margin_down[i]), True, (0, 0, 0))
        rect_down = down.get_rect()
        rect_down.topleft = ((MARGIN + SQUARE_SIZE) * (1 + i) + MARGIN + 20, (MARGIN + SQUARE_SIZE) * 11)
        screen.blit(down, rect_down)

        side = arialfont.render('{}'.format(margin_side[i]), True, (0, 0, 0))
        rect_side = side.get_rect()
        rect_side.topleft = (15, (MARGIN + SQUARE_SIZE) * i + 15)
        screen.blit(side, rect_side)


class Board:
    def __init__(self):
        self.board = []  # 2d board
        self.grid = grid
        self.silver_left = 20
        self.gold_left = 12
        self.king_left = 1
        self.king_pos = (5, 5)
        self.king_moved = 0
        self.king_distance_edge = 0
        self.king_open = 0
        self.king_mobility = 4
        self.winner = None
        self.stats = []
        self.set_board()
        self.score = 0

    # draws tiles without the pieces
    def draw_tiles(self, screen):
        screen.fill((200, 200, 200))
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                color = WHITE
                if grid[row][col] == '*':
                    color = GREEN
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + SQUARE_SIZE) * (col + 1) + MARGIN,
                                  (MARGIN + SQUARE_SIZE) * row + MARGIN,
                                  SQUARE_SIZE,
                                  SQUARE_SIZE])

    # sets the pieces on the board
    def set_board(self):
        for row in range(len(grid)):
            self.board.append([])
            for column in range(len(grid[row])):
                if grid[row][column] == 'G':
                    self.board[row].append(Piece(row, column, 'G'))
                elif grid[row][column] == 'S':
                    self.board[row].append(Piece(row, column, 'S'))
                elif grid[row][column] == 'K':
                    self.board[row].append(Piece(row, column, 'K'))
                elif grid[row][column] == '-':
                    self.board[row].append('-')
                elif grid[row][column] == '*':
                    self.board[row].append('*')

    # draws the board with the set pieces
    def draw(self, screen):
        self.draw_tiles(screen)
        for row in range(len(grid)):
            for column in range(len(grid[row])):
                if self.board[row][column] not in {'-', '*'}:
                    piece = self.board[row][column]
                    piece.draw(screen)

    # returns the contents at a given row, col
    def get_tile(self, row, column):
        return self.board[row][column]

    # moves a piece to row, col
    def move(self, piece, row, col):
        if piece in {'-', '*'}:
            pass
        else:
            self.board[row][col] = self.board[piece.row][piece.col]

            if piece.row in {0, 10} or piece.col in {0, 10}:
                self.board[piece.row][piece.col] = '*'
            else:
                self.board[piece.row][piece.col] = '-'

            piece.move(row, col)
            if piece.king:
                self.king_pos = (row, col)
                # self.get_king_distance()
            king_moves, king_captures = self.get_valid_actions(self.get_tile(self.king_pos[0], self.king_pos[1]))
            self.king_mobility = len(king_moves)

            self.check_winner()

    # removes a piece when captured
    def remove(self, row, col):
        piece_to_remove = self.board[row][col]
        if piece_to_remove.piece_type == 'S':
            self.silver_left -= 1

        elif piece_to_remove.piece_type == 'G':
            if piece_to_remove.king:
                self.king_left -= 1
            else:
                self.gold_left -= 1

        if row in {0, 10} or col in {0, 10}:
            self.board[row][col] = '*'
        else:
            self.board[row][col] = '-'

    # returns all valid actions = moves + captures
    def get_valid_actions(self, piece):
        r = piece.row
        c = piece.col
        moves = self.find_moves(r, c) + self.find_moves(r, c, 1)
        captures = self.find_capture(piece)
        return moves, captures

    def find_capture(self, piece):
        captures = []
        r = piece.row
        c = piece.col

        if c + 1 < len(self.board):
            if r - 1 > 0:
                if self.board[r - 1][c + 1] not in {'-', '*'}:
                    if self.board[r - 1][c + 1].piece_type != piece.piece_type:
                        captures.append((r - 1, c + 1))

            if r + 1 < len(self.board):
                if self.board[r + 1][c + 1] not in {'-', '*'}:
                    if self.board[r + 1][c + 1].piece_type != piece.piece_type:
                        captures.append((r + 1, c + 1))

        if c - 1 > 0:
            if r - 1 > 0:
                if self.board[r - 1][c - 1] not in {'-', '*'}:
                    if self.board[r - 1][c - 1].piece_type != piece.piece_type:
                        captures.append((r - 1, c - 1))

            if r + 1 < len(self.board):
                if self.board[r + 1][c - 1] not in {'-', '*'}:
                    if self.board[r + 1][c - 1].piece_type != piece.piece_type:
                        captures.append((r + 1, c - 1))

        return captures

    def find_moves(self, r, c, direction=0):
        moves = []
        if self.board[r][c] in {'-', '*'}:
            return moves

        can_go = True
        can_go_pos = True
        can_go_neg = True

        i, j = 0, 0

        if direction == 1:
            i = 1
        else:
            j = 1

        while can_go:
            if r + i > len(self.board) - 1 or c + j > len(self.board) - 1:
                can_go_pos = False
            elif can_go_pos:
                if self.board[r + i][c + j] in {'-', '*'}:
                    moves.append((r + i, c + j))
                else:
                    can_go_pos = False

            if r - i < 0 or c - j < 0:
                can_go_neg = False
            elif can_go_neg:
                if self.board[r - i][c - j] in {'-', '*'}:
                    moves.append((r - i, c - j))
                else:
                    can_go_neg = False

            if not can_go_pos and not can_go_neg:
                can_go = False

            if direction == 1:
                i += 1
            else:
                j += 1

        return moves

    def get_all_valid_actions(self, turn):
        # print('here')
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] not in {'-', '*'}:
                    current_piece = self.board[row][col]

                    if turn.piece_just_moved is not None:
                        if (current_piece.row, current_piece.col) == \
                                (turn.piece_just_moved.row, turn.piece_just_moved.col):
                            continue

                        if current_piece.king and turn.piece_just_moved.piece_type == 'G':
                            continue
                    # print(current_piece)
                    if current_piece.piece_type == turn.current_player:
                        moves, captures = self.get_valid_actions(current_piece)

                        # some randomness
                        random.shuffle(moves)
                        random.shuffle(captures)

                        if turn.moves_made == 0:
                            current_valid_actions = (moves, captures)
                        else:
                            current_valid_actions = (moves, [])

                        # check if not empty in case that a piece is blocked
                        if not current_valid_actions:
                            continue



                        turn.all_actions.update({current_piece: current_valid_actions})

    def evaluate(self):
        # gold player is maximising

        king_pos = self.find_king()

        # king stats
        king_mobility = 0  # moves available
        king_surrounded = 0  # captures available
        king_distance_edge = self.get_king_distance()  # distance to the closest edge
        king_exposed = 0  # enemy pieces at the end of king's movement path

        if self.king_left >= 1:
            king_moves, king_captures = self.get_valid_actions(self.get_tile(king_pos[0], king_pos[1]))
            king_mobility = len(king_moves)
            king_surrounded = len(king_captures)
            king_distance_edge = self.king_distance_edge
            king_exposed = self.king_exposed(king_moves)

        escaped = 1000 if self.winner == 'G' else 0
        captured = -1000 if self.winner == 'S' else 0

        # if escaped:
        #     return escaped
        # if captured:
        #     return captured

        return -5 * (king_surrounded + 1) + king_mobility - 2 * king_exposed - 3 * king_distance_edge \
               + (10*self.gold_left - 2*self.silver_left) + escaped + captured

    def king_exposed(self, king_moves):
        exposed = 0

        min_row = self.king_pos[0]
        max_row = self.king_pos[0]

        min_col = self.king_pos[1]
        max_col = self.king_pos[1]

        for row, col in king_moves:

            # for row
            if self.king_pos[0] == row:
                min_col = min(min_col, col)
                max_col = max(max_col, col)

            # for col
            elif self.king_pos[1] == col:
                min_row = min(min_row, row)
                max_row = max(max_row, row)

        # check king's column
        if min_row not in {self.king_pos[0], 0}:
            if self.board[min_row - 1][self.king_pos[1]] not in {'-', '*'}:
                if self.board[min_row - 1][self.king_pos[1]].piece_type == 'S':
                    exposed += 1

        if max_row not in {self.king_pos[0], 10}:
            if self.board[max_row + 1][self.king_pos[1]] not in {'-', '*'}:
                if self.board[max_row + 1][self.king_pos[1]].piece_type == 'S':
                    exposed += 1

        # check king's row
        if min_col not in {self.king_pos[1], 0}:
            if self.board[self.king_pos[0]][min_col - 1] not in {'-', '*'}:
                if self.board[self.king_pos[0]][min_col - 1].piece_type == 'S':
                    exposed += 1

        if max_col not in {self.king_pos[1], 10}:
            if self.board[self.king_pos[0]][max_col + 1] not in {'-', '*'}:
                if self.board[self.king_pos[0]][max_col + 1].piece_type == 'S':
                    exposed += 1

        return exposed

    def get_king_distance(self):
        c_d = self.king_pos[0] if self.king_pos[0] <= 5 else 10 - self.king_pos[0]
        r_d = self.king_pos[1] if self.king_pos[1] <= 5 else 10 - self.king_pos[1]
        self.king_distance_edge = min(c_d, r_d)
        return min(c_d, r_d)

    def check_winner(self):
        if self.king_left == 0:
            self.winner = 'S'
            return 'S'

        k_pos = self.find_king()
        if k_pos[0] in {0, 10} or k_pos[1] in {0, 10}:
            self.winner = 'G'
            return 'G'

        else:
            return None

    def find_king(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] not in {'-', '*'}:
                    if self.board[row][col].king:
                        self.king_pos = (row, col)
                        return row, col
