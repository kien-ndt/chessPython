import tkinter as tk
import chess
import numpy as np

console_board = chess.Board()
# canvas góc phần tư 4 oxy
class GUI:
    rows = 8
    columns = 8
    dim_square = 64

    images = {}
    color1 = "#DDB88C"
    color2 = "#A66D4F"
    piece_legal_move_color = "#6EFA93"
    selected_piece_color = "#42C264"
    piece_legal_move = []
    selected_piece = None       # dạng kí tự string ô chọn h1, a1
    focused = None

    def __init__(self, parent, chessboard):
        self.console_board = chessboard                         # chess ban đầu của thư viện
        self.set_chess_board(chessboard)                        # chuyển đổi sang mảng np
        canvas_width = (self.columns + 1) * self.dim_square
        canvas_height = (self.rows + 1) * self.dim_square
        self.canvas = tk.Canvas(parent, width=canvas_width, height=canvas_height)
        self.canvas.pack(padx=8, pady=8)
        self.draw_board()
        self.draw_pieces(self.chessboard)

        self.canvas.tag_lower("area")

        self.canvas.tag_raise("occupied")

        self.canvas.bind("<Button-1>", self.square_clicked)

    def set_chess_board(self, board_chess_lib):
        board = str(board_chess_lib).replace("\n", " ").split()
        board = np.array(board).reshape([8, 8])
        self.chessboard = board

    def draw_board(self):
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.dim_square)
                y1 = (row * self.dim_square)
                x2 = x1 + self.dim_square
                y2 = y1 + self.dim_square
                if (col, row) in self.piece_legal_move:
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                                                 fill=self.piece_legal_move_color,
                                                 tags="area")
                else:
                    if self.selected_piece is not None and (col, row) == self.string_name_to_number_pos(self.selected_piece):
                        self.canvas.create_rectangle(x1, y1, x2, y2,
                                                     fill=self.selected_piece_color,
                                                     tags="area")
                    else:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color,
                                                                     tags="area")
                color = self.color1 if color == self.color2 else self.color2

        for row in range(self.rows):
            x = ((self.columns + 1) * self.dim_square) - int(self.dim_square / 2)
            y = (row * self.dim_square) + int(self.dim_square / 2)
            self.canvas.create_text(x, y, text=str(8-row), anchor=tk.CENTER)
        for column in range(self.columns):
            x = (column * self.dim_square) + int(self.dim_square / 2)
            y = ((row + 1) * self.dim_square) + int(self.dim_square / 2)
            self.canvas.create_text(x, y, text=str(chr(ord('a') + column)), anchor=tk.CENTER)
        self.canvas.tag_raise("occupied")
        self.canvas.tag_lower("area")
        self.piece_legal_move = []

    def draw_pieces(self, chessboard): # chessboard: np array
        self.canvas.delete("occupied")
        self.images = {}
        for i, row in enumerate(chessboard):
            for j, element in enumerate(row):
                if element and str(element).isalpha():
                    occupied_name = str(element) + str(i) + str(j)
                    self.images[occupied_name] = self.get_pieces_image(str(element))
                    self.canvas.create_image(0, 0, image=self.images[occupied_name],
                                             tags=(occupied_name, "occupied"),
                                             anchor="c")
                    x_canvas = j
                    y_canvas = i
                    x0 = (x_canvas * self.dim_square) + int(self.dim_square / 2)
                    y0 = (y_canvas * self.dim_square) + int(self.dim_square / 2)
                    self.canvas.coords(occupied_name, x0, y0)

    def get_pieces_image(self, name):
        pieces_img_dir = "./pieces_image/"
        name = str(name)
        if str(name).isupper():
            img_path = pieces_img_dir + name.lower() + "white.png"
        else:
            img_path = pieces_img_dir + name + "black.png"
        return tk.PhotoImage(file=img_path)

    def square_clicked(self, event):
        col_size = row_size = self.dim_square
        selected_column = int(event.x / col_size)
        selected_row = int(event.y / row_size)
        if self.selected_piece is None:
            self.get_piece_legal_moves(selected_column, selected_row)
            if len(self.piece_legal_move) == 0:
                return
            self.selected_piece = self.number_to_string_name_pos(selected_column, selected_row)
        else:
            res_move = self.move(self.selected_piece, self.number_to_string_name_pos(selected_column, selected_row))
            self.selected_piece = None
        self.draw_board()

    def number_to_string_name_pos(self, col, row):              # chuyển số hàng số cột sang dạng chữ + số a1 a2...
        s_row = str(8 - row)
        s_col = str(chr(ord('a') + col))
        s = s_col + s_row
        return s

    def string_name_to_number_pos(self, string_pos):
        s_col = string_pos[0]
        s_row = string_pos[1]
        col = ord(s_col) - ord('a')
        row = 8 - int(s_row)
        return col, row

    def move(self, from_square, to_square):                 # di chuyển quân cờ (ví dụ h1 h2)
        try:
            self.console_board.push_san(from_square + to_square)
        except:
            return False
        self.set_chess_board(self.console_board)
        self.draw_pieces(self.chessboard)
        return True

    def get_piece_legal_moves(self, col, row):
        pos = self.number_to_string_name_pos(col, row)
        list_legal_moves = list(self.console_board.legal_moves)
        piece_legal_moves = []
        for legal_move in list_legal_moves:
            if str(legal_move)[0:2] == pos:
                piece_legal_moves.append(self.string_name_to_number_pos(str(legal_move)[2:4]))
        self.piece_legal_move = piece_legal_moves

def main():
    root = tk.Tk()
    root.title("Chess")
    gui = GUI(root, console_board)
    root.mainloop()


if __name__ == "__main__":
    main()
