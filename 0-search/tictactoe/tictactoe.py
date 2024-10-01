"""
Tic Tac Toe Player
"""

import random
import copy

X = "X"
O = "O"
EMPTY = None

board_cache = {}


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Two variables to keep track of how many turns each player has had
    count_x, count_o = 0, 0

    # Loop through all cells on the board, counting the X's and O's
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count_x += 1
            elif board[i][j] == O:
                count_o += 1

    # If the number of X's and O's are equal, we know it's X's turn.
    # Otherwise, it's O's turn.
    if count_x == count_o:
        return X

    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Keep track of empty cells using this set
    empty_cells = set()

    # Loop through all cells on the board, storing empty cells
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                empty_cells.add((i, j))

    # Shuffle actions so our AI behaves differently each time
    return empty_cells


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Destructure action tuple
    i, j = action

    # Check if action is valid
    if i < 0 or i > 2 or j < 0 or j > 2 or board[i][j] != EMPTY:
        raise Exception(f"action {action} is invalid")

    # Get the next player
    next_player = player(board)

    # Create a copy of the current board and apply action to it
    board_copy = copy.deepcopy(board)
    board_copy[i][j] = next_player

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check cache for efficiency
    key = str(board)
    if key in board_cache:
        return board_cache[key]

    # Check columns
    for col in range(3):
        count_x, count_o = 0, 0
        for row in range(3):
            if board[row][col] == X:
                count_x += 1
            elif board[row][col] == O:
                count_o += 1
        if count_x == 3:
            board_cache[key] = X
            return X
        elif count_o == 3:
            board_cache[key] = O
            return O

    # Check rows
    for row in range(3):
        count_x, count_o = 0, 0
        for col in range(3):
            if board[row][col] == X:
                count_x += 1
            elif board[row][col] == O:
                count_o += 1
        if count_x == 3:
            board_cache[key] = X
            return X
        elif count_o == 3:
            board_cache[key] = O
            return O

    # Check top left to bottom right diagonal
    topleft_to_bottomright = [board[0][0], board[1][1], board[2][2]]

    count_x, count_o = 0, 0
    for cell in topleft_to_bottomright:
        if cell == X:
            count_x += 1
        elif cell == O:
            count_o += 1

    if count_x == 3:
        board_cache[key] = X
        return X
    elif count_o == 3:
        board_cache[key] = O
        return O

    # Check top right to bottom left diagonal
    topright_to_bottomleft = [board[0][2], board[1][1], board[2][0]]

    count_x, count_o = 0, 0
    for cell in topright_to_bottomleft:
        if cell == X:
            count_x += 1
        elif cell == O:
            count_o += 1

    if count_x == 3:
        board_cache[key] = X
        return X
    elif count_o == 3:
        board_cache[key] = O
        return O

    # If we reach this statement, there's no winner
    board_cache[key] = None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there's a winner, the board is terminal
    if winner(board) is not None:
        return True

    # Loop through all cells on the board, any empty cells means the board is
    # not terminal
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False

    # No winner, and no empty cells, the board is terminal
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)

    if winning_player == X:
        return 1

    if winning_player == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    _, best_action = helper(board)
    return best_action


def helper(board):
    """
    A helper function for the minimax function. Takes a board state
    and returns the best action available by recursing until a winning
    terminal state is found. The first action found that can result in
    a win is returned.
    """
    # If our state is a terminal board, return its utility
    if terminal(board):
        return (utility(board), None)

    next_player = player(board)

    # Value, Action tuple (-inf for X, +inf for O)
    v = (float("-inf") if next_player == X else float("inf"), None)

    # Run the minimax algorithm on all available moves
    possible_actions = list(actions(board))
    random.shuffle(possible_actions)
    for action in possible_actions:
        if next_player == X:
            temp = helper(result(board, action))
            if v[0] < temp[0]:
                v = (temp[0], action)

            # Alpha-beta pruning, no need to consider other moves if we've
            # already found an ideal move.
            if v[0] == 1:
                return v
        else:
            temp = helper(result(board, action))
            if v[0] > temp[0]:
                v = (temp[0], action)
            if v[0] == -1:
                return v

    return v
