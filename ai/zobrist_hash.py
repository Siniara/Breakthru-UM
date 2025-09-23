import random
random.seed(1)

zobTable = [[[random.randint(1, 2**64 - 1) for i in range(3)]for j in range(11)]for k in range(11)]


def indexing(piece):
    if piece.piece_type == 'G':
        if piece.king:
            return 2
        else:
            return 1
    elif piece.piece_type == 'S':
        return 0


def compute_hash(board):
    h = 0
    for i in range(11):
        for j in range(11):
            if board[i][j] not in {'-', '*'}:
                piece = indexing(board[i][j])
                h ^= zobTable[i][j][piece]
    return h


if __name__ == "__main__":
    for i in zobTable:
        print(i)
