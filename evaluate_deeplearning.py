import chess
import numpy as np
import table
import random
import time

#https://www.tensorflow.org/install/pip#virtual-environment-install
#https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow_cpu-2.7.0-cp38-cp38-manylinux2010_x86_64.whl
from keras.models import Sequential, load_model, model_from_json

class Evaluate:
    chess_dict = {
        'p' : [1,0,0,0,0,0,0,0,0,0,0,0],
        'P' : [0,0,0,0,0,0,1,0,0,0,0,0],
        'n' : [0,1,0,0,0,0,0,0,0,0,0,0],
        'N' : [0,0,0,0,0,0,0,1,0,0,0,0],
        'b' : [0,0,1,0,0,0,0,0,0,0,0,0],
        'B' : [0,0,0,0,0,0,0,0,1,0,0,0],
        'r' : [0,0,0,1,0,0,0,0,0,0,0,0],
        'R' : [0,0,0,0,0,0,0,0,0,1,0,0],
        'q' : [0,0,0,0,1,0,0,0,0,0,0,0],
        'Q' : [0,0,0,0,0,0,0,0,0,0,1,0],
        'k' : [0,0,0,0,0,1,0,0,0,0,0,0],
        'K' : [0,0,0,0,0,0,0,0,0,0,0,1],
        '.' : [0,0,0,0,0,0,0,0,0,0,0,0],
    }
    maximum = 9000.0
    minimum = -6818.0
    def __init__(self):
        self.model = self.load_keras_model('mse', 'Adam')
        # self.model = self.load_keras_model('binary_crossentropy', 'Adam')

    
    def evaluate_board(self, board):
        board = board.copy()
        matrix = self.make_matrix(board.copy())
        translated = np.array(self.translate(matrix,self.chess_dict))
        # start = time.time()

        # score = self.model.predict(translated.reshape(1,8,8,12))

        score = self.model(translated.reshape(1,8,8,12))
        score = np.array(score)
        # print(time.time() - start)

        value_pieces_score = self.all_piece_values(board)

        if score[0][0]:
            return score[0][0]*(self.maximum-self.minimum)+self.minimum + value_pieces_score
        else:
            return value_pieces_score

    def load_keras_model(self,loss,optimizer):
        json_file = open('./chess_best_model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        model.compile(optimizer=optimizer, loss=loss, metrics = None)
        model.load_weights('./chess_best_model.h5')
        return model

    def make_matrix(self,board):
        pgn = board.epd()
        foo = []
        pieces = pgn.split(" ", 1)[0]
        rows = pieces.split("/")
        for row in rows:
            foo2 = []
            for thing in row:
                if thing.isdigit():
                    for i in range(0, int(thing)):
                        foo2.append('.')
                else:
                    foo2.append(thing)
            foo.append(foo2)
        return foo

    def translate(self, matrix,chess_dict):
        rows = []
        for row in matrix:
            terms = []
            for term in row:
                terms.append(chess_dict[term])
            rows.append(terms)
        return rows

    def all_piece_values(self, board):
        board = board.copy()
        value_pieces_score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)

            if piece is not None:
                piece_symbol = piece.symbol()
                if piece_symbol.islower():  # neu la den thi -
                    piece_score = -1
                else:
                    piece_score = 1
                if piece_symbol.lower() == 'p':
                    piece_score *= 100*1.2
                elif piece_symbol.lower() == 'n':
                    piece_score *= 300*1.2
                elif piece_symbol.lower() == 'b':
                    piece_score *= 300*1.2
                elif piece_symbol.lower() == 'r':
                    piece_score *= 500*1.2
                elif piece_symbol.lower() == 'q':
                    piece_score *= 900*1.2
                elif piece_symbol.lower() == 'k':
                    piece_score *= 10000*1.2

                value_pieces_score += piece_score

        return value_pieces_score


# board = chess.Board("8/8/5k2/3n1p2/4p3/2n5/5K2/2B5 b - - 1 67")
# eval = Evaluate()
# print(eval.evaluate_board(board))

#============================================================================================
    def calculate_move(self, depth,board,epochs):
        node=0
        first_legal_moves = str(board.legal_moves)[39:-2].replace(',','').split()
        scores = [[0]] * len(first_legal_moves)
        for epoch in range(epochs):
            for first_move in range(len(first_legal_moves)):
                play_board = board.copy()
                play_board.push_san(first_legal_moves[first_move])
                for _ in range(depth):
                    legal_moves = str(play_board.legal_moves)[39:-2].replace(',','').split()
                    try:
                        move = random.choice(legal_moves)
                        play_board.push_san(move)
                    except:
                        # scores[first_move] *= 1000
                        # scores[first_move] += self.model.predict(translated.reshape(1,8,8,12))*(self.maximum-self.minimum)+self.minimum
                        # node+=1
                        break

                matrix = self.make_matrix(play_board.copy())                
                translated = np.array(self.translate(matrix,self.chess_dict))

                scores[first_move] += self.model.predict(translated.reshape(1,8,8,12))*(self.maximum-self.minimum)+self.minimum
                node+=1
            # print('Epoch',str(epoch+1)+'/'+str(epochs))
        print(node)
        return str(first_legal_moves[scores.index(max(scores))])

