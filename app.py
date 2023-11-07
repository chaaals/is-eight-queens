from tkinter import *
from pathlib import Path
from typing import Literal

from algorithm.eight_queens import EightQueens
from utils.get_tile_image import get_tile_image

class App():
    def __init__(self, root: Tk):
        self.root = root
        self.eight_queens = EightQueens()
        self.board = self.eight_queens.board
        self.solution_board = [[ None for _ in range(8)] for _ in range(8)]
        self.tiles = [[ Button for _ in range(8)] for _ in range(8)]

        self.bgImage = PhotoImage(file="assets/bgImage.png")
        self.bgLabel = Label(root, image=self.bgImage)

    # Frames
    def start_frame(self, root: Tk, **props):
        def on_start_click():
            self.clear_screen(frame=self.root, skip=[self.bgLabel])
            self.board_frame(root=self.root, board=self.board, mode='active')

        def on_history_click():
            self.clear_screen(frame=self.root, skip=[self.bgLabel])
            self.history_viewer_frame(self.root)

        start_label = Label(root, border = 0, bg = "#000000", text='Eight Queens Puzzle', fg='#FFFFFF', font = ('Henny Penny', 45))
        start_label.place(x=248, y=288)

        history_button = Button(root, border = 0, width = 9, height = 0, text="Start Game", bg = "#000000", cursor = 'hand2', fg='#FFFFFF', command=on_start_click, font = ('Montserrat', 18))
        history_button.place(x=357, y=415)

        history_button = Button(root, border = 0, width = 9, height = 0, text="History", bg = "#000000", cursor = 'hand2', fg='#FFFFFF', command=on_history_click, font = ('Montserrat', 18))
        history_button.place(x=557, y=415)

    def board_frame(self, root: Tk, board: list[list[dict]], coord: tuple = (220, 36), mode: Literal['active', 'disabled'] = 'active', **props):
        play_frame = Frame(root)

        x, y = coord
        play_frame.place(x=x, y=y)

        def on_save_board():
            self.eight_queens.export_board()
            self.on_reset_board()

        def on_back():
            self.eight_queens.reset_board()
            self.on_reset_board()
            self.clear_screen(root, skip=[self.bgLabel])
            self.start_frame(root=self.root)
            
        self.render_board(play_frame, board=board, mode=mode)

        saveButton = Button(root, border = 0, width = 9, height = 2, text="Save", bg = "#000000", cursor = 'hand2', fg='#FFFFFF', command=on_save_board, font = ('Montserrat', 18))
        saveButton.place(x=910, y=36)

        resetButton = Button(root, border = 0, width = 9, height = 2, text="Reset", bg = "#000000", cursor = 'hand2', fg='#FFFFFF', command=self.on_reset_board, font = ('Montserrat', 18))
        resetButton.place(x=910, y=112)

        backButton = Button(root, border = 0, width = 9, height = 2, text="Back", bg = "#000000", cursor = 'hand2', fg='#FFFFFF', command=on_back, font = ('Montserrat', 18))
        backButton.place(x=910, y=188)

    def history_viewer_frame(self, root: Tk, **props):
        board_frame = Frame(root)
        board_frame.place(x=365, y=36)

        self.eight_queens.file_to_board()

        def view_solution(event):
            index, = nav_bar.curselection()
            self.solution_board = self.eight_queens.imported_boards[index]
            self.update_board(board=self.solution_board)

        def on_back():
            self.solution_board = [[ None for _ in range(8)] for _ in range(8)]
            self.clear_screen(root, skip=[self.bgLabel])
            self.start_frame(root=self.root)
            
        width, height = 23, root.winfo_height()
        answers = tuple([f"Board {i + 1}" for i in range(len(self.eight_queens.imported_boards))])
        
        lb_var = Variable(value=answers)

        nav_frame = Frame(root)
        nav_frame.pack()
        nav_frame.place(x=0, y=0)

        nav_bar = Listbox(nav_frame, width=width, listvariable=lb_var, selectmode=SINGLE, border=0, bg="#EBECD0", font=('Montserrat', 12))
        nav_bar.pack(side=LEFT, fill=Y, expand=True)

        backButton = Button(root, border = 0, width = 9, height = 2, text="Back", bg = "#000000", cursor = 'hand2', fg='#FFFFFF', command=on_back, font = ('Montserrat', 18))
        backButton.place(x=20, y=220)

        scroll_bar = Scrollbar(nav_frame, command=nav_bar.yview, orient='vertical')
        scroll_bar.pack(side=RIGHT, fill=Y)

        nav_bar.config(yscrollcommand=scroll_bar.set)
        nav_bar.bind('<<ListboxSelect>>', view_solution)

        self.render_board(frame=board_frame, board=self.solution_board, mode='disabled')

    # Global functions
    def on_reset_board(self):
        self.eight_queens.reset_board()
        self.board = self.eight_queens.board
            
        self.update_board(board=self.board)
        
    def on_tile_click(self, row: int, col: int):
        is_killzone_or_empty = self.board[row][col]['id'] is None or self.board[row][col]['id'] == 'killzone'

        if is_killzone_or_empty:
            self.eight_queens.place_queen(row, col)
        else:
            self.eight_queens.remove_queen(row,col)

        self.update_board(board=self.board)

    def update_board(self, board: list[list[dict]]):
        for row in range(len(board)):
            for col in range(len(board[row])):
                tile_image = get_tile_image(board[row][col]['asset'])
                self.tiles[row][col].config(image=tile_image)
                self.tiles[row][col].image = tile_image

    def render_board(self, frame: Frame, board: list[list[dict]], **props):
        bg = None
        tile_image = PhotoImage(None)
        
        for row in range(len(board)):
            for col in range(len(board[row])):
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                    bg = "#779556"
                else:
                    bg = "#EBECD0"

                tile = None
                tile = Button(frame, border=0, image=tile_image, width=80, height=80, bg = bg, command=lambda r=row, c=col: self.on_tile_click(r, c))

                if props['mode'] and props['mode'] == 'disabled':
                    tile = Label(frame, border=0, image=tile_image, width=80, height=80, bg = bg)
                else:
                    tile = Button(frame, border=0, image=tile_image, width=80, height=80, bg = bg, command=lambda r=row, c=col: self.on_tile_click(r, c))

                tile.image = tile_image
                tile.grid(row=row, column=col)

                self.tiles[row][col] = tile


    def clear_screen(self, frame: Tk, skip: list[Widget]):
        for widget in frame.winfo_children():
            if any(widget == s for s in skip):
                continue

            widget.destroy()

    # Run function
    def run(self): 
        # start app
        self.root.title('Eight Queens Puzzle')

        self.root.geometry("1080x720+120+50")
        self.root.resizable(0,0)

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.bgLabel.image = self.bgImage
        self.bgLabel.pack()

        self.start_frame(root=self.root)

if __name__ == '__main__':
    root = Tk()

    app = App(root)
    app.run()

    root.mainloop()