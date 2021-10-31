class Piece:
    pieces_img_dir = "./pieces_image/"

    # chess_name = ['r', 'n', 'b', 'q', 'k', 'p', 'R', 'N', 'B', 'Q', 'K', 'P']

    def get_piece_image_dir(self, name):
        name = str(name)
        if str(name).isupper():
            return self.pieces_img_dir + name.lower() + "white.png"
        else:
            return self.pieces_img_dir + name + "black.png"
