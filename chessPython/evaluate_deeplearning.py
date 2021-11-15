import chess
import numpy as np
import table
#https://www.tensorflow.org/install/pip#virtual-environment-install
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
    
    def evaluate_board(self, board):
        matrix = self.make_matrix(board.copy())
        translated = np.array(self.translate(matrix,self.chess_dict))
        score = self.model.predict(translated.reshape(1,8,8,12))*(self.maximum-self.minimum)+self.minimum

        # for square in chess.SQUARES:

        if score[0][0]:
            return score[0][0]
        else:
            return 0

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


# board = chess.Board("8/8/5k2/3n1p2/4p3/2n5/5K2/2B5 b - - 1 67")
# eval = Evaluate()
# print(eval.evaluate_board(board))