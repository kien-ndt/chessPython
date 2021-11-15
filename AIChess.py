import copy

import chess
import PositionScore as pos_score
# import board as eval_board
from evaluate_deeplearning import Evaluate
class AIChess:

    INFINITY = 9999999
    global_depth = 2
    global_next_move = None
    global_turn = 'w'           # quan tinh loi the
    number_nodes = 0

    def __init__(self):
        self.eval = Evaluate()

    def get_next_move_minimax(self, board):
        global global_turn
        global number_nodes
        number_nodes = 0
        if board.turn:
            global_turn = 'w'
        else:
            global_turn = 'b'
        self.minimax(board, self.global_depth, -self.INFINITY, self.INFINITY, True)
        print(number_nodes)
        return global_next_move


    def minimax(self, board, depth, alpha, beta, maximizing_player):
        global number_nodes
        if depth == 0 or not board.legal_moves:
            return self.evaluate(board, global_turn)

        list_legal_moves = list(board.legal_moves)
        if maximizing_player:
            max_val = -self.INFINITY
            for move in list_legal_moves:
                board.push_san(str(move))
                number_nodes+=1
                val = self.minimax(board, depth - 1, alpha, beta, False)

                if depth == self.global_depth:
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
            min_val = self.INFINITY
            for move in list_legal_moves:
                board.push_san(str(move))
                self.number_nodes+=1
                val = self.minimax(board, depth - 1, alpha, beta, True)
                min_val = min(min_val, val)
                beta = min(beta, val)
                board.pop()
                if beta <= alpha:
                    break
            return min_val

    def evaluate(self, board, global_turn):
        score = self.eval.evaluate_board(board)
        print(score)
        if global_turn == 'w':
        # return eval_board.evaluate_board(board, global_turn)
            return score
        else:
            return -score

