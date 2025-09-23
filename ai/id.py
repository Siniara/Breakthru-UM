import copy
import random
import time
random.seed(1)

def it_deepening(turn, game, time_limit):
    start = time.time()

    MAX, MIN = 1000, -1000

    def minimax2(turn, depth, alpha, beta, game):
        if time.time() - start >= time_limit:
            score = turn.current_board.evaluate(None)
            return score, turn

        # zhash = computeHash(turn.current_board.board)
        # if zhash in game.ttable and game.ttable[zhash][1] >= depth:
        #     print('yes')
        #     return game.ttable[zhash][0], turn

        if depth == 0 or turn.current_board.check_winner() is not None:
            score = turn.current_board.evaluate(None)
            return score, turn

        max_player = True if turn.current_player == 'G' else False
        if max_player:
            max_score = MIN
            best_state = None
            piece_to_move = None

            # generates children
            states = get_all_states2(turn)
            #order moves
            for state, piece in states:
                score = minimax2(state, depth - 1, alpha, beta, game)[0]
                max_score = max(max_score, score)
                if max_score == score:
                    best_state = state
                    piece_to_move = piece

                alpha = max(alpha, max_score)
                # if beta <= alpha:
                #     # print('alpha prune', depth)
                #     break

            # zhash = computeHash(turn.current_board.board)
            # if zhash in game.ttable and game.ttable[zhash][1] < depth:
            #     game.ttable.update({zhash: [max_score, depth]})
            # elif zhash not in game.ttable:
            #     game.ttable.update({zhash: [max_score, depth]})

            return max_score, best_state, piece_to_move

        else:
            min_score = MAX
            best_state = None
            piece_to_move = None

            # generates children
            states = get_all_states2(turn)
            # order moves

            for state, piece in states:

                score = minimax2(state, depth - 1, alpha, beta, game)[0]
                # print('min:', min_score)
                min_score = min(min_score, score)
                if min_score == score:
                    best_state = state
                    piece_to_move = piece

                beta = min(beta, min_score)
                # if beta <= alpha:
                #     # print('beta prune', depth)
                #     break

            # zhash = computeHash(turn.current_board.board)
            # if zhash in game.ttable and game.ttable[zhash][1] < depth:
            #     game.ttable.update({zhash:[min_score, depth]})
            # elif zhash not in game.ttable:
            #     game.ttable.update({zhash: [min_score, depth]})


            return min_score, best_state, piece_to_move



    # score, next_state, piece_to_move = None, None, None
    last_best = None
    depth = 1
    while True:
        if time.time() - start >= time_limit:
            break

        turn.current_board.get_all_valid_actions()
        score, next_state, piece_to_move = minimax2(turn, depth, -1000, 1000, game)

        # get children
        # states = get_all_states2(turn)
        # for state in states:
        #     score, next_state, piece_to_move = minimax2(state,depth,-1000,1000)

        last_best = score, next_state, piece_to_move
        print(depth, 'last best', last_best)
        depth += 1

    print('depth', depth)
    return last_best



# either two moves or 1 capture


def simulate_turn(turn, piece, move):
    turn.selected_piece = piece
    moves, captures = turn.current_board.get_valid_actions(piece)
    turn.valid_actions = moves + captures
    turn.select_move(move[0], move[1])

    turn.current_board.check_winner()
    turn.update_turn()
    turn.current_board.get_all_valid_actions(turn)



    return turn


# def simulate_action(piece, move, board):
#
#     if board[move[0]][move[1]] in {'*', '-'}:
#         board.move(piece, move[0], move[1])
#
#     else:
#         board.remove(move[0], move[1])
#         board.move(piece, move[0], move[1])
#
#     return board




# I only need boards after, wrong because I need to keep generating new children
def get_all_states2(turn):
    states = []
    # only boards = []
    # print(turn.all_actions)
    # print('')
    for piece in turn.all_actions:
        # valid_actions = copy.deepcopy(turn.all_actions)
        # print(valid_actions)
        # print(piece)
        valid_actions = turn.all_actions[piece][0] + turn.all_actions[piece][1]
        # print(valid_actions)
        for action in valid_actions:
            # print(piece, action)

            temp_board = copy.deepcopy(turn.current_board)

            temp_turn = copy.deepcopy(turn)
            temp_turn.current_board = temp_board

            temp_piece = temp_turn.current_board.get_tile(piece.row, piece.col)
            new_state = simulate_turn(temp_turn, temp_piece, action)

            # new_state = turn.simulate_action(temp_piece, action[0], action[1])

            states.append((new_state, piece))

            # if piece.king:
            #     states.insert(0, (new_state, piece))
            # else:
            #     states.append((new_state, piece))

    return states

zobTable = [[[random.randint(1,2**64 - 1) for i in range(3)]for j in range(11)]for k in range(11)]

def indexing(piece):
    if piece.piece_type == 'G':
        if piece.king:
            return 2
        else:
            return 1
    elif piece.piece_type == 'S':
        return 0

def computeHash(board):
    h = 0
    for i in range(11):
        for j in range(11):
            # print(i,j)
           # print board[i][j]
            if board[i][j] not in {'-', '*'}:
                piece = indexing(board[i][j])
                h ^= zobTable[i][j][piece]
    return h
