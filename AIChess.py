import copy

import chess
import PositionScore as pos_score
import time
# import board as eval_board
from evaluate_deeplearning import Evaluate
class AIChess:

    INFINITY = 9999999
    global_depth = 4
    global_next_move = None
    global_turn = 'w'           # quan tinh loi the
    number_nodes = 0
    global_eval_time = 0
    global_eval_count = 0
    global_start_time = 0

    def __init__(self):
        self.eval = Evaluate()

    def get_next_move_minimax(self, board):
        start_time = time.time()
        print("Calculating...............")
        global global_turn
        global global_next_move 
        global_next_move= None
        self.number_nodes = 0
        if board.turn:
            global_turn = 'w'
        else:
            global_turn = 'b'
        # return self.eval.calculate_move(8, board.copy(), 50)
        self.global_eval_time=0
        self.global_eval_count=0
        self.sum_time=0
        self.global_start_time=time.time()
        self.minimax(board, self.global_depth, -self.INFINITY, self.INFINITY, True)
        print(self.number_nodes, time.time()-start_time, self.global_eval_time, self.global_eval_count, self.sum_time)
        return global_next_move


    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or not board.legal_moves or (depth<=1 and time.time() - self.global_start_time > 30):
            if not board.legal_moves:
                if board.outcome():
                    winner = board.outcome().winner
                    if winner == True:
                        if self.global_turn == 'w':
                            return self.INFINITY
                        else:
                            return -self.INFINITY
                    else:
                        if self.global_turn == 'w':
                            return -self.INFINITY
                        else:
                            return self.INFINITY
                            
            start1 = time.time()
            k = self.evaluate(board, global_turn)
            self.global_eval_count+=1
            self.global_eval_time+=time.time() - start1
            return k

        list_legal_moves = list(board.legal_moves)
        if maximizing_player:
            max_val = -self.INFINITY
            for move in list_legal_moves:
                board.push_san(str(move))
                self.number_nodes+=1
                val = self.minimax(board, depth - 1, alpha, beta, False)

                if depth == self.global_depth:
                    if val >= max_val:
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
        score = self.eval.evaluate_board(board, self.get_sum_eval_time)
        # print(score)
        if global_turn == 'w':
        # return eval_board.evaluate_board(board, global_turn)
            return score
        else:
            return -score
    sum_time = 0
    def get_sum_eval_time(self, sum_time):
        self.sum_time += sum_time

