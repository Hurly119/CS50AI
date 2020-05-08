"""
Tic Tac Toe Player
"""

import math
import random

X = "X"
O = "O"
EMPTY = None
moves = 0

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
    moves = 0

    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] != EMPTY:
                moves+=1

    if moves % 2 == 0:
        return X
    return O

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = []
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == EMPTY:
                possibleActions.append((row,column))
    return set(possibleActions)
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    playersPiece = player(board)
    newBoard = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

    for row in range(len(board)):
        for column in range(len(board[row])):
            newBoard[row][column] = board[row][column]


    row,column = action

    if newBoard[row][column] == EMPTY:
        newBoard[row][column] = playersPiece
    else:
        raise Exception("Invalid action.")
    return newBoard
    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in range(len(board)):
        if board[row].count(X) == 3:
            return X
        elif board[row].count(O) == 3:
            return O
        for column in range(len(board[row])):
            if board[0][column] == X and board[1][column] == X and board[2][column] == X:
                return X
            elif board[0][column] == O and board[1][column] == O and board[2][column] == O:
                return O

    if (board[0][0] == X and board[1][1] ==X and board[2][2] ==X) or (board[0][2] == X and board[1][1]==X and board[2][0] ==X):
        return X

    elif (board[0][0] == O and board[1][1] == O and board[2][2] == O) or (board[0][2] == O and board[1][1]== O and board[2][0] ==O):
        return O

    else: return None



    # raise NotImplementedError


def terminal(board):
    if winner(board) is None:
        for row in range(len(board)):
            for column in range(len(board[row])):
                if board[row][column] == EMPTY:
                    return False
    return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)== X:
        return 1
    elif winner(board)== O:
        return -1
    else: return 0

    # raise NotImplementedError

def maxValue(board):
    if terminal(board):
        return (utility(board))

    value = float("-inf")

    for action in actions(board):
        value = max(value,minValue(result(board,action)))
        if value == 1:
            return value
    return value


def minValue(board):
    if terminal(board):
        return (utility(board))

    value = float("inf")

    for action in actions(board):
        value = min(value,maxValue(result(board,action)))
        if value == -1:
            return value
    return value



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    move = None
    if player(board) == X:
        highValue = float("-inf")
        for action in actions(board):
            value = minValue(result(board,action))
            if value == 1:
                move =  action
                highValue = value
            elif value >= highValue:
                move = action
                highValue = value

    else:
        lowValue = float("inf")
        for action in actions(board):
            value = maxValue(result(board, action))
            if value == -1:
                move = action
                lowValue = value
            elif value <= lowValue:
                move = action
                lowValue = value
    return move





    # raise NotImplementedError
