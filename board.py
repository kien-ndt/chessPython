import chess

import table

    
def evaluate_board(board, turn):
    return sum(
        piece_value(board.piece_at(square), square, turn)
        if board.piece_at(square) is not None else 0
        for square in chess.SQUARES)


def piece_value(piece, square, turn):
    symbol = piece.symbol()
    if turn == 'w':
        is_white = not symbol.islower()

        row = convert_square(square, is_white)[0]
        column = convert_square(square, is_white)[1]

        score = 1 if is_white else -1
        if symbol.lower() == 'p':
            score *= (1000 + table.PAWN[row][column])
        elif symbol.lower() == 'n':
            score *= (3000 + table.KNIGHT[row][column])
        elif symbol.lower() == 'b':
            score *= (3000 + table.BISHOP[row][column])
        elif symbol.lower() == 'r':
            score *= (5000 + table.ROOK[row][column])
        elif symbol.lower() == 'q':
            score *= (9000 + table.QUEEN[row][column])
        elif symbol.lower() == 'k':
            score *= (1000000 + table.KING[row][column])
        return score
    else:
        is_black = symbol.islower()

        row = convert_square(square, is_black)[0]
        column = convert_square(square, is_black)[1]

        score = 1 if is_black else -1
        if symbol.lower() == 'p':
            score *= (1000 + table.PAWN[::-1][row][column])
        elif symbol.lower() == 'n':
            score *= (3000 + table.KNIGHT[::-1][row][column])
        elif symbol.lower() == 'b':
            score *= (3000 + table.BISHOP[::-1][row][column])
        elif symbol.lower() == 'r':
            score *= (5000 + table.ROOK[::-1][row][column])
        elif symbol.lower() == 'q':
            score *= (9000 + table.QUEEN[::-1][row][column])
        elif symbol.lower() == 'k':
            score *= (1000000 + table.KING[::-1][row][column])
        return score


def convert_square(square, is_white):
    row = 7 - (square // 8) if is_white else square // 8
    column = square % 8
    return (row, column)