from ai.zobrist_hash import compute_hash
from ai.simulate_action import get_all_states


MIN = -1000
def nega_max(turn, depth, alpha, beta, game):
    alpha_original = alpha

    zhash = compute_hash(turn.current_board.board)
    if zhash in game.ttable and game.ttable[zhash][0] >= depth:
        tt_entry = game.ttable[zhash]
        tt_flag = tt_entry[2]
        tt_value = tt_entry[1]
        if tt_flag == 'exact':
            # print('exact')
            return tt_value, tt_entry[3], tt_entry[4]
        elif tt_flag == 'lower_bound':
            # print('lower')
            alpha = max(alpha, tt_value)
        elif tt_flag == 'upper_bound':
            # print('upper')
            beta = min(beta, tt_value)

        if beta <= alpha:
            # print('yes')
            return tt_value, tt_entry[3], tt_entry[4]

    # point of view of max or min/gold maximises the objective function
    pov = 1 if turn.current_player == 'G' else -1

    if depth == 0 or turn.current_board.check_winner() is not None:
        score = pov * turn.current_board.evaluate()
        return score, None, None

    max_score = MIN
    best_move = None
    piece_to_move = None

    # generates children
    states = get_all_states(turn)
    # order moves by eval function
    if pov == 1:
        states.sort(key=lambda x: x[0], reverse=True)
    else:
        states.sort(key=lambda x: x[0], reverse=False)

    for value, state, piece in states:

        if state.current_player != turn.current_player:
            score = -nega_max(state, depth - 1, -beta, -alpha, game)[0]
        else:
            score = nega_max(state, depth - 1, alpha, beta, game)[0]

        if score > max_score:
            max_score = score
            best_move = state.piece_just_moved.row, state.piece_just_moved.col
            piece_to_move = piece

        alpha = max(alpha, max_score)
        if beta <= alpha:
            # print('prune', depth)
            break

    zhash = compute_hash(turn.current_board.board)
    tt_score = max_score
    if tt_score <= alpha_original:
        flag = 'upper_bound'
    elif tt_score >= beta:
        flag = 'lower_bound'
    else:
        flag = 'exact'

    game.ttable.update({zhash: [depth, tt_score, flag, best_move, piece_to_move]})

    return max_score, best_move, piece_to_move
