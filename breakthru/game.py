import pygame
from .board import Board, draw_margins
from .turn import Turn
from .grid import margin_side, margin_side_num, margin_down_num, margin_down
from ai.players import HumanPlayer


class Game:
    def __init__(self, screen, players=(HumanPlayer('S'), HumanPlayer('G'))):
        self.screen = screen
        self.players = players
        self._init()

    def update(self):
        self.board.draw(self.screen)
        draw_margins(self.screen, margin_down, margin_side)
        self.turn.draw_valid_actions(self.turn.valid_actions)

        self.turn.draw_turn_color()

        #  draws the action
        if self.turn.piece_just_moved:
            self.turn.draw_just_moved()
        pygame.display.update()

    def _init(self):
        self.board = Board()
        self.winner = None
        self.turns = 0
        self.actions = 0
        self.turn = Turn(self.board, self.screen)
        self.history = []
        self.history_chess = []
        self.ttable = {}

    def reset(self):
        self._init()

    def init_move(self, row=None, col=None):
        player1, player2 = self.players

        player_g = player1 if player1.player_color == 'G' else player2
        player_s = player1 if player1.player_color == 'S' else player2

        if self.winner is None:

            if self.turn.current_player == 'S':
                if player_s.human:
                    player_s.get_move(self.turn, row, col)

                elif not player_s.human:
                    player_s.get_move(self.turn)

            elif self.turn.current_player == 'G':
                if player_g.human:
                    player_g.get_move(self.turn, row, col)

                elif not player_g.human:
                    player_g.get_move(self.turn)

            self.winner = self.turn.update_turn(self)

        if self.actions > 0:

            if self.winner is not None:
                print('Game history, {} actions'.format(self.actions))
                for event in self.history_chess:
                    piece, row, column = event
                    print(piece, ': ', row, column)
                print('Winner:', self.winner, '; {} actions'.format(self.actions), '; {} turns'.format(self.turns))

                # self.save_log()

    def update_history(self, selected):

        moved_from = self.turn.piece_just_moved_from
        moved_to = (selected.row, selected.col)

        chess_moved_from = (margin_down[moved_from[1]], margin_side[moved_from[0]])
        chess_moved_to = (margin_down[moved_to[1]], margin_side[moved_to[0]])

        if self.turn.piece_just_moved.king:
            self.history.append(('K', moved_from, moved_to))
            self.history_chess.append(('K', chess_moved_from, chess_moved_to))
        else:
            self.history.append((self.turn.current_player, moved_from, moved_to))
            self.history_chess.append((self.turn.current_player, chess_moved_from, chess_moved_to))

        self.actions += 1

    def undo_move(self):
        # does not undo a capture!!
        row, col = self.turn.piece_just_moved_from
        self.turn.current_board.move(self.turn.piece_just_moved, row, col)

        if self.turn.moves_made == 0:
            self.turn.change_turn()
            self.turns -= 1
        else:
            self.turn.moves_made -= 1

        self.turn.piece_just_moved = None

        self.actions -= 1
        self.history.pop(-1)

    def save_log(self):
        # overwrites the previous
        print('History log created')
        log = self.history_chess
        out = open("logs/game_hist.txt", "w")
        out.write('Game history')
        out.write('\n')
        out.write('Winner: ' + str(self.winner) + '; {} actions'.format(self.actions)
                  + '; {} turns'.format(self.turns))
        out.write('\n')
        k = 1
        for i in log:
            out.write(str(k) + ': ' + str(i))
            out.write('\n')
            print(i)
            k += 1
        out.close()
