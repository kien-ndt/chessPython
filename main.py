import chess

board = chess.Board()
# board.turn: true => white, false => black
# k=list(board.legal_moves)[0]
# print(k.to_square)
#board.push_san()
#   a b c d e f g h
# 8
# 7
# 6
# 5
# 4
# 3
# 2
# 1
row = [8, 7, 6, 5, 4, 3, 2, 1]
column = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

k=list(board.legal_moves)[0]
print(k.to_square)
board.push_san('h1h7')
print(board)
# boardarr = str(board).replace("\n", " ").split()
# boardarr = np.array(boardarr).reshape([8, 8])
# print(boardarr[0][0])
