from ai.simulate_action import get_all_states


MAX, MIN = 1000, -1000
def minimax(turn, depth, alpha, beta, game):

    if depth == 0 or turn.current_board.check_winner() is not None:
        score = turn.current_board.evaluate()
        return score, None, None

    max_player = True if turn.current_player == 'G' else False
    if max_player:
        max_score = alpha
        best_move = None
        piece_to_move = None

        # generate children
        states = get_all_states(turn)
        #order moves by eval funct score
        states.sort(key=lambda x: x[0], reverse=True)

        for value, state, piece in states:

            score = minimax(state, depth - 1, alpha, beta, game)[0]

            if score > max_score:
                max_score = score
                best_move = state.piece_just_moved.row, state.piece_just_moved.col
                piece_to_move = piece

            alpha = max(alpha, max_score)
            if beta <= alpha:
                # print('max prune', depth)
                break

        return max_score, best_move, piece_to_move

    else:
        min_score = beta
        best_move = None
        piece_to_move = None

        # generate children
        states = get_all_states(turn)
        # order moves
        states.sort(key=lambda x: x[0], reverse=False)

        for value, state, piece in states:

            score = minimax(state, depth - 1, alpha, beta, game)[0]

            if score < min_score:
                min_score = score
                best_move = state.piece_just_moved.row, state.piece_just_moved.col
                piece_to_move = piece

            beta = min(beta, min_score)
            if beta <= alpha:
                # print('min prune', depth)
                break

        return min_score, best_move, piece_to_move
