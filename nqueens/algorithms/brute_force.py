def brute_force(nqueens):
    N = nqueens.N
    solutions = []
    _brute_force_helper(N, [], solutions)
    if solutions:
        nqueens.board = solutions[0]
        return True
    return False

def _brute_force_helper(N, current_board, solutions):
    if len(current_board) == N:
        if is_valid_board(current_board):
            solutions.append(current_board[:])
        return

    for col in range(N):
        new_board = current_board + [col]
        _brute_force_helper(N, new_board, solutions)

def is_valid_board(board):
    for row1 in range(len(board)):
        for row2 in range(row1 + 1, len(board)):
            col1 = board[row1]
            col2 = board[row2]
            if col1 == col2 or abs(row1 - row2) == abs(col1 - col2):
                return False
    return True