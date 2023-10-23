from tkinter import *

from algorithm.eight_queens import EightQueens
from utils.get_tile_image import get_tile_image

class App():
    def __init__(self, root: Tk):
        self.eight_queens = EightQueens()
        self.board = self.eight_queens.board
        self.tiles = [[ Button for _ in range(8)] for _ in range(8)]

        root.title('Eight Queens Puzzle')

        self.run(root)

        root.geometry("1080x720+120+50")
        root.resizable(0,0)

        root.protocol("WM_DELETE_WINDOW", root.destroy)

    def on_tile_click(self, row: int, col: int):
        is_killzone_or_empty = self.eight_queens.board[row][col]['id'] is None or self.eight_queens.board[row][col]['id'] == 'killzone'

        if is_killzone_or_empty:
            self.eight_queens.place_queen((row, col))
        else:
            self.eight_queens.remove_queen((row,col))

        self.update_board()

    def update_board(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                tile_image = get_tile_image(self.board[row][col]['asset'])
                self.tiles[row][col].config(image=tile_image)
                self.tiles[row][col].image = tile_image

    def render_board(self, frame: Frame):
        bg = None
        tile_image = PhotoImage(None)
        
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                    bg = "#779556"
                else:
                    bg = "#EBECD0"

                button = Button(frame, border=0, image=tile_image, width=80, height=80, bg = bg, command=lambda r=row, c=col: self.on_tile_click(r, c))

                button.image = tile_image
                button.grid(row=row, column=col)

                self.tiles[row][col] = button

    def board_frame(self, root: Tk, coord: tuple = (220, 36)):
        play_frame = Frame(root)

        x, y = coord
        play_frame.place(x=x, y=y)

        self.render_board(play_frame)

    def solutions_viewer_frame(self, root: Tk):
        # render UI for solutions viewer

        # Steps:
        # 1. Get all solutions from eight queens (self.imported_boards)
        # 2. Extract board to be viewed from imported boards
        self.board_frame(root=root,coord=(375, 36))
        pass

    def clear_screen(self, frame: Tk, skip: list[Widget]):
        for widget in frame.winfo_children():
            if any(widget == s for s in skip):
                continue

            widget.destroy()

    def run(self, root: Tk): 
        bgImage = PhotoImage(file="assets/bgImage.png")
        bgLabel = Label(root, image = bgImage)
        bgLabel.image = bgImage
        bgLabel.pack()

        def on_start_click():
            self.clear_screen(frame=root, skip=[bgLabel])
            self.board_frame(root)

        def on_solutions_click():
            # TODO: Implement solutions viewer
            # self.eight_queens.generate_answers()
            # self.solutions_viewer_frame()
            self.clear_screen(frame=root, skip=[bgLabel])
            self.solutions_viewer_frame(root)
            pass

        startLabel = Label(root, border = 0, bg = "#000000", text='Eight Queens Puzzle', fg='#FFFFFF', font = ('Henny Penny', 45))
        startLabel.place(x=248, y=288)

        startButton = Button(root, border = 0, width = 9, height = 0, text="Start Game", bg = "#000000", cursor = 'hand2', fg='#FFFFFF', command=on_start_click, font = ('Montserrat', 18))
        startButton.place(x=357, y=415)

        solutionsButton = Button(root, border = 0, width = 9, height = 0, text="Solutions", bg = "#000000", cursor = 'hand2', fg='#FFFFFF', command=on_solutions_click, font = ('Montserrat', 18))
        solutionsButton.place(x=557, y=415)

if __name__ == '__main__':
    root = Tk()
    bgImage = PhotoImage(file="assets/bgImage.png")
    Label(root, image = bgImage).pack()
    app = App(root)
    root.mainloop()