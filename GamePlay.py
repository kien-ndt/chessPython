import GUI
import tkinter as tk
import chess

root = tk.Tk()
root.title("Chess")
gui = GUI.GUI(root, chess.Board())
root.mainloop()