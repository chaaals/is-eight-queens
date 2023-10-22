from pathlib import Path
from tkinter import *
from tkinter import ttk
from algorithm.eight_queens import EightQueens

class App():
    def __init__(self, root: Tk):
        root.title('Eight Queens Puzzle')

        self.start_window(root)
        self.play(root)

        root.geometry("1080x720+120+50")
        root.resizable(0,0)

        root.protocol("WM_DELETE_WINDOW", root.destroy)

        self.eight_queens = EightQueens()

    def on_tile_click(self, row: int, col: int):
        # TODO: Implement place queen and remove queen logic
        print(row, col)

    def render_board(self, frame: Frame):
        board = [[None for _ in range(8)] for _ in range(8)]
        # TODO: replace with board from algorithm
        # buttons = self.eight_queens.board()

        # TODO: remove, should be based on asset propert from board
        test_asset = Path.cwd() / 'assets' / 'black_queen.png'

        bg = None
        for row in range(len(board)):
            for col in range(len(board[row])):
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                    bg = "#779556"
                else:
                    bg = "#EBECD0"

                pv = PhotoImage(file=test_asset)

                button = Button(frame, border=0, image=pv, width=80, height=80, bg = bg, command=lambda r=row, c=col: self.on_tile_click(r, c))

                button.image = pv
                button.grid(row=row, column=col)

    def play(self, root: Tk):
        play_frame = Frame(root)
        play_frame.place(x=220, y=36)

        self.render_board(play_frame)

    def start_window(self, root: Tk):
        root.withdraw()
        start_window = Toplevel()
        start_window.title('Start')
        start_window.geometry("1080x720+120+50")
        start_window.resizable(0,0)

        def startGame():
            start_window.destroy()
            root.deiconify()

        startButton = Button(start_window, border = 0, width = 23, text="Start Game", bg = "#FF89DB", cursor = 'hand2', fg='#FFFFFF', command=startGame, font = ('Blinker', 18))
        startButton.place(x=390, y=590)


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()