import copy

import chess
import PositionScore as pos_score
import board as eval_board
INFINITY = 9999999
global_depth = 4
global_next_move = None
global_turn = 'w'
number_nodes = 0

def get_next_move_minimax(board):
    global global_turn
    global number_nodes
    number_nodes = 0
    if board.turn:
        global_turn = 'w'
    else:
        global_turn = 'b'
    minimax(board, global_depth, -INFINITY, INFINITY, True)
    print(number_nodes)
    return global_next_move


def minimax(board, depth, alpha, beta, maximizing_player):
    global number_nodes
    if depth == 0 or not board.legal_moves:
        return evaluate(board)

    list_legal_moves = list(board.legal_moves)
    if maximizing_player:
        max_val = -INFINITY
        for move in list_legal_moves:
            board.push_san(str(move))
            number_nodes+=1
            val = minimax(board, depth - 1, alpha, beta, False)

            if depth == global_depth:
                if val > max_val:
                    global global_next_move
                    global_next_move = str(move)

            max_val = max(max_val, val)
            alpha = max(alpha, val)
            board.pop()
            if beta <= alpha:
                break
        return max_val
    else:
        min_val = INFINITY
        for move in list_legal_moves:
            board.push_san(str(move))
            number_nodes+=1
            val = minimax(board, depth - 1, alpha, beta, True)
            min_val = min(min_val, val)
            beta = min(beta, val)
            board.pop()
            if beta <= alpha:
                break
        return min_val

def evaluate(board):
    return eval_board.evaluate_board(board)

