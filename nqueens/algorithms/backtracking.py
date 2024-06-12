def backtracking(nqueens, row):
    return _backtracking_helper(nqueens, row)


def _backtracking_helper(nqueens, row):
    if row == nqueens.N:
        return True
    for col in range(nqueens.N):                        # for each row, check all (row, col) positions
        if nqueens.is_valid(row, col):
            nqueens.board.append(col)                   # if a valid one is found, add it to the board config
            if _backtracking_helper(nqueens, row + 1):  # call helper recursively
                return True
            nqueens.board.pop()       # it reverses the append operation, and tries another position of queen in the same column backtracks to the last queen position
    return False