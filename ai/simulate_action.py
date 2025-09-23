import copy


def simulate_action(turn, piece, move):
    turn.selected_piece = piece
    moves, captures = turn.current_board.get_valid_actions(piece)
    turn.valid_actions = moves + captures
    turn.select_move(move[0], move[1])

    turn.current_board.check_winner()
    turn.update_turn()
    turn.current_board.get_all_valid_actions(turn)

    return turn


def get_all_states(turn):
    states = []
    for piece in turn.all_actions:
        valid_actions = turn.all_actions[piece][0] + turn.all_actions[piece][1]
        for action in valid_actions:
            temp_board = copy.deepcopy(turn.current_board)
            temp_turn = copy.deepcopy(turn)
            temp_turn.current_board = temp_board
            temp_piece = temp_turn.current_board.get_tile(piece.row, piece.col)
            new_state = simulate_action(temp_turn, temp_piece, action)
            new_state_score = new_state.current_board.evaluate()

            states.append((new_state_score, new_state, piece))


    return states


