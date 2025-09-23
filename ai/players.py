import random
import time
from ai.minimax import minimax
from ai.id import it_deepening
from ai.negamax import nega_max
from ai.id_nm import it_deepening_nm


class Player:
    def __init__(self, color):
        self.player_color = color

    @staticmethod
    def select_random_move(actions):
        selected_piece = random.choice(list(actions))
        all_actions = actions[selected_piece][0] + actions[selected_piece][1]
        selected_action = random.choice(all_actions)
        valid_actions = all_actions

        return selected_piece, selected_action, valid_actions

    @staticmethod
    def move(turn, selected_piece, selected_action, valid_actions):
        turn.selected_piece = selected_piece
        turn.valid_actions = valid_actions
        turn.select_move(selected_action[0], selected_action[1])


class HumanPlayer(Player):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'Human Player'
        self.human = True

    @staticmethod
    def get_move(turn, row, col):
        if 0 <= row <= 10 and 0 <= col <= 10:
            turn.select_move(row, col)
            return row, col
        return None

    def __str__(self):
        return "Player color: " + str(self.player_color) + ", Player type:" + self.name


class RandomPlayer(Player):
    def __init__(self, color):
        super().__init__(color)
        self.player_color = color
        self.human = False
        self.name = "Random Player"

    def get_move(self, turn):
        turn.current_board.get_all_valid_actions(turn)
        actions = turn.all_actions

        start = time.time()
        selected_piece, selected_action, valid_actions = self.select_random_move(actions)
        end = time.time()
        print('RP:', end - start)

        self.move(turn, selected_piece, selected_action, valid_actions)

        return selected_piece, selected_action, valid_actions

    def __str__(self):
        return "Player color: " + str(self.player_color) + ", Player type:" + self.name


class RandomPlayerPlus(Player):
    def __init__(self, color):
        super().__init__(color)
        self.player_color = color
        self.human = False
        self.name = "Random Player Plus"

    def get_move(self, turn):
        turn.current_board.get_all_valid_actions(turn)
        actions = turn.all_actions
        # print(actions)
        for piece in actions:
            if piece.king:
                for move in actions[piece][0]:
                    row, col = move
                    if row in {0, 10} or col in {0, 10}:
                        selected_piece = piece
                        selected_action = (row, col)
                        valid_actions = actions[selected_piece][0] + actions[selected_piece][1]

                        self.move(turn, selected_piece, selected_action, valid_actions)

                        return selected_piece, selected_action, valid_actions

            for capture in turn.current_board.find_capture(piece):
                if turn.current_board.board[capture[0]][capture[1]].king:
                    selected_piece = piece
                    selected_action = (capture[0], capture[1])
                    valid_actions = actions[selected_piece][0] + actions[selected_piece][1]

                    self.move(turn, selected_piece, selected_action, valid_actions)

                    return selected_piece, selected_action, valid_actions

        selected_piece, selected_action, valid_actions = self.select_random_move(actions)
        self.move(turn, selected_piece, selected_action, valid_actions)

        return selected_piece, selected_action, valid_actions

    def __str__(self):
        return "Player color: " + str(self.player_color) + ", Player type:" + self.name


class MiniMaxPlayer(Player):
    def __init__(self, color, depth, game):
        super().__init__(color)
        self.player_color = color
        self.human = False
        self.name = "MiniMax Player"
        self.search_depth = depth
        self.game = game

    def get_move(self, turn):
        turn.current_board.get_all_valid_actions(turn)

        start = time.time()
        score, next_move, piece_to_move = minimax(self.game.turn, self.search_depth, -1000, 1000, self.game)
        end = time.time()
        print('MM:', end - start)
        print(score, next_move, piece_to_move)
        # print('')

        move = next_move
        moves, captures = turn.current_board.get_valid_actions(piece_to_move)
        piece_valid_actions = moves + captures

        self.move(turn, piece_to_move, move, piece_valid_actions)

        return piece_to_move, move, piece_valid_actions

    def __str__(self):
        return "Player color: " + str(self.player_color) + ", Player type:" + self.name


class NegaMaxPlayer(Player):
    def __init__(self, color, depth, game):
        super().__init__(color)
        self.player_color = color
        self.human = False
        self.name = "NegaMax Player"
        self.search_depth = depth
        self.game = game

    def get_move(self, turn):
        turn.current_board.get_all_valid_actions(turn)

        start = time.time()
        score, next_move, piece_to_move = nega_max(self.game.turn, self.search_depth, -1000, 1000, self.game)
        end = time.time()
        print('NM:', end - start)
        print(score, next_move, piece_to_move)
        # print('')

        move = next_move
        moves, captures = turn.current_board.get_valid_actions(piece_to_move)
        piece_valid_actions = moves + captures

        self.move(turn, piece_to_move, move, piece_valid_actions)

        return piece_to_move, move, piece_valid_actions

    def __str__(self):
        return "Player color: " + str(self.player_color) + ", Player type:" + self.name


class ItDeepPlayer(Player):
    def __init__(self, color, game, time):
        super().__init__(color)
        self.player_color = color
        self.human = False
        self.name = "Iterative Deepening Player"
        self.time_limit = time
        self.game = game

    def get_move(self, turn):
        turn.current_board.get_all_valid_actions(turn)

        start = time.time()

        score, next_move, piece_to_move = it_deepening_nm(self.game.turn, self.game, self.time_limit)

        end = time.time()


        print('NM:', end - start)

        # print('******************')
        # print('')
        print(score, next_move, piece_to_move)
        # for key in vars(next_state):
        #     print(key, vars(next_state)[key])
        # print('')

        move = next_move
        moves, captures = turn.current_board.get_valid_actions(piece_to_move)
        piece_valid_actions = moves + captures

        self.move(turn, piece_to_move, move, piece_valid_actions)

        return piece_to_move, move, piece_valid_actions

    def __str__(self):
        return "Player color: " + str(self.player_color) + ", Player type:" + self.name