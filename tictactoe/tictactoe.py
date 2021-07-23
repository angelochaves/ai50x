"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    contX = 0
    contO = 0

    if terminal(board) == True:
        return

    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                contX = contX + 1
            elif board[i][j] == O:
                contO = contO + 1

    if contX > contO:
        return O
    elif contX == contO:
        return X
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                actions.add((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    deepBoard = copy.deepcopy(board)
    try:
        if deepBoard[action[0]][action[1]] != EMPTY:
            raise ValueError
        else:
            deepBoard[action[0]][action[1]] = player(deepBoard)
            return deepBoard
    except ValueError:
        print("Move already made!")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Tests horizontally
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][0] == board[i][2]:
            return board[i][0]
    # Tests vertically
    for j in range(3):
        if board[0][j] == board[1][j] and board[0][j] == board[2][j]:
            return board[0][j]
    # Tests diagonally
    if (board[1][1] == board[0][0] and board[1][1] == board[2][2]) or (board[1][1] == board[0][2] and board[1][1] == board[2][0]):
        return board[1][1]
    return None


def fullBoard(board):
    vacant = 0
    for row in board:
        vacant += row.count(EMPTY)
    if vacant == 0:
        return True
    else:
        return False


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or fullBoard(board) == True:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def maxi(board, beta):
    if terminal(board):
        return utility(board)
    alpha = -math.inf
    for action in actions(board):
        alpha = max(alpha, mini(result(board, action), alpha))
        if beta <= alpha:
            return alpha
    return alpha


def mini(board, alpha):
    if terminal(board):
        return utility(board)
    beta = math.inf
    for action in actions(board):
        beta = min(beta, maxi(result(board, action), beta))
        if beta <= alpha:
            return beta
    return beta


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        alpha = -math.inf
        for action in actions(board):
            beta = mini(result(board, action), alpha)
            if beta > alpha:
                alpha = beta
                optimal = action
    elif player(board) == O:
        beta = math.inf
        for action in actions(board):
            alpha = maxi(result(board, action), beta)
            if alpha < beta:
                beta = alpha
                optimal = action
    return optimal