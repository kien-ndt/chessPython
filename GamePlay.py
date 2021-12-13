import GUI
import tkinter as tk
import chess

root = tk.Tk()
root.title("Chess")
gui = GUI.GUI(root, chess.Board("7k/8/5PP1/R7/8/7P/8/6K1 w KQkq - 0 1"))
# gui = GUI.GUI(root, chess.Board())
root.mainloop()