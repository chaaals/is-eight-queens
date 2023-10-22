from pathlib import Path
from datetime import datetime

class EightQueens():
    'description'

    def __init__(self, size: int = 8):
        self._size = size
        self._queen_positions = []
        self._board = [[{}]]
        self._generate_board()

        self._valid_queen_asset = Path("path/to/valid/queen/asset")
        self._invalid_queen_asset = Path("path/to/invalid/queen/asset")
        self._killzone_asset = Path("path/to/killzone/asset")
    
    @property
    def size(self) -> int:
        'return size of the row and column of the board'
        return self._size

    @property
    def board(self) -> list[list[dict]]:
        'return generated/updated board'
        return self._board

    @property
    def queens(self) -> list[tuple[int,int]]:
        'returns a list of the positions (x,y) of all queens present in the board'
        return self._queen_positions

    def reset_board(self):
        'generates a new board with blank tiles'
        self._generate_board()

    def place_queen(self, row: int, column: int):
        """
        Places a queen and their respective killzones on the board.
        Killzones can overlap and queens can be placed on killzones

        Args:
            position (tuple): row and column where the queen should be placed.
        Raises:
            ValueError: If the specified position is already occupied by another queen.
        """
        self._validate_position(row, column)

        occupied = self._board[row][column]["id"] == "queen"
        if occupied:
            ALREADY_OCCUPIED = f"This tile ({row},{column}) already has a queen. It has {self._board[row][column]['id']} as the id\nDid you mean to use 'remove_queen()' instead?"
            raise ValueError(ALREADY_OCCUPIED)
        
        position = (row, column)
        self._queen_positions.append(position)
        self._board[row][column]["id"] = "queen"

        def add_killzone(row: int, column: int):
            '''
            helper subfunction to add a killzone based on position given
            also checks if tile is empty beforehand to avoid replacing a queen's id with a killzone from other queens
            '''
            self._board[row][column]["value"] += 1

            is_tile_empty = self._board[row][column]["id"] != "queen"
            if is_tile_empty:
                self._board[row][column]["id"] = "killzone"
                self._board[row][column]["asset"] = self._killzone_asset


        # row killzone
        for i in range(self.size):
            queen_killzone = (row, i)
            placed_queen = (row, column)

            if queen_killzone != placed_queen:
                add_killzone(row, i)

            # columns
            # if (i, column) != placed_queen:
            #     self._board[row][i]["value"] += 1
            #     add_killzone(i, column)

        # column killzone
        for i in range(self.size):
            queen_killzone = (i, column)
            placed_queen = (row, column)

            if queen_killzone != placed_queen:
                add_killzone(i, column)
        
        # quadrant 1 (upper right)
        i=1
        while row-i>=0 and column+i<self.size:
            add_killzone(row-i, column+i)
            i += 1

        # quadrant 2 (upper left)
        i=1
        while row-i>=0 and column-i>=0:
            add_killzone(row-i, column-i)
            i += 1

        # quadrant 3 (bottom right)
        i=1
        while row+i<self.size and column-i>=0:
            add_killzone(row+i, column-i)
            i += 1

        # quadrant 4 (bottom left)
        i=1
        while row+i<self.size and column+i<self.size:
            add_killzone(row+i, column+i)
            i += 1

        self._validate_queens()

    def remove_queen(self, row: int, column: int):
        """
        Removes a queen and their respective killzones on the board.
        Removed killzones that overlapped with other killzones won't remove those other killzones

        Args:
            position (tuple): row and column of the queen to be removed.
        Raises:
            ValueError: If the specified position is not occupied by a queen.
        """
        self._validate_position(row, column)
        
        occupied = self._board[row][column]["id"] == "queen"
        if not occupied:
            EMPTY_TILE = f"This tile ({row},{column}) does not have a queen. It has {self._board[row][column]['id']} as the id\nDid you mean to use 'place_queen()' instead?"
            raise ValueError(EMPTY_TILE)
        
        position = (row, column)
        self._queen_positions.pop(self._queen_positions.index(position))
        self._board[row][column]["id"] = None

        removed_queen_was_killzone = self._board[row][column]["value"] > 0
        if removed_queen_was_killzone:
            self._board[row][column]["id"] = "killzone"
            self._board[row][column]["asset"] = self._killzone_asset

        def remove_killzone(row: int, column: int):
            '''
            helper subfunction to remove a killzone based on position given
            also to avoid replacing asset of an invalid queen when removing a killzone
            '''
            self._board[row][column]["value"] -= 1

            is_removed_killzone_empty = self._board[row][column]["value"] == 0 and self._board[row][column]["asset"] == self._killzone_asset
            if is_removed_killzone_empty:
                self._board[row][column]["id"] = None
                self._board[row][column]["asset"] = None

        for i in range(self.size):
            queen_killzone = (row, i)
            placed_queen = (row, column)

            if queen_killzone != placed_queen:
                remove_killzone(row, i)

        # column killzone
        for i in range(self.size):
            queen_killzone = (i, column)
            placed_queen = (row, column)

            if queen_killzone != placed_queen:
                remove_killzone(i, column)
        
        # quadrant 1 (upper right)
        i=1
        while row-i>=0 and column+i<self.size:
            remove_killzone(row-i, column+i)
            i += 1

        # quadrant 2 (upper left)
        i=1
        while row-i>=0 and column-i>=0:
            remove_killzone(row-i, column-i)
            i += 1

        # quadrant 3 (bottom right)
        i=1
        while row+i<self.size and column-i>=0:
            remove_killzone(row+i, column-i)
            i += 1

        # quadrant 4 (bottom left)
        i=1
        while row+i<self.size and column+i<self.size:
            remove_killzone(row+i, column+i)
            i += 1

        self._validate_queens()
    
    def set_assets(self, valid_queen: str, invalid_queen: str, killzone: str):
        'set image paths to valid_queen, invalid_queen, and killzone assets'
        self._valid_queen_asset = Path(valid_queen).resolve()
        self._invalid_queen_asset = Path(invalid_queen).resolve()
        self._killzone_asset = Path(killzone).resolve()

    def generate_answers(self):
        def generate(row: int = 0) -> bool:

            # base case
            if row >= self.size:
                return
            
            board_row = self._board[row]
            is_last_row = row == self.size - 1

            for i in range(self.size):
                tile = board_row[i]

                if tile['value'] == 0:
                    print(f"place_queen({row}, {i})")
                    self.place_queen(row, i)
                    all_8_queens_valid = self._validate_queens() and len(self.queens) == 8

                    if is_last_row and all_8_queens_valid:
                        self.export_board()
                    
                    generate(row+1)
                    self.remove_queen(row, i)
            
            # return is_solution
        generate()

    def export_board(self):
        export_path = Path(f'./boards/board_{datetime.now().strftime(r"%Y%m%d_%H%M%S%f")}.txt')
        Path.mkdir(export_path.parent, exist_ok=True, parents=True)

        with open(export_path, "w") as file:
            for row in self.board:
                for value in row:
                    if value['id'] == "queen":
                        file.write("Q\t")

                    elif value['id'] == "killzone":
                        file.write(".\t")

                    else:
                        file.write("!\t")

                file.write("\n")

    def file_to_board(self, file: Path):
        pass

    def _generate_board(self):
        'description'
        self._board = [[{
            "id": None,
            "value": 0,
            "asset": None
            } for _ in range(8)
        ] for _ in range(8)]
    
    def _validate_position(self, row: int, column: int):
        'interrupt process if not a valid position'
        position = (row, column)

        all_int = all([isinstance(value, int) for value in position])
        if not all_int:
            raise ValueError("Position should be 2 ints (position in x and y)")

        out_of_bounds = all(value > self.size for value in position)
        if out_of_bounds:
            raise ValueError(f"Position is out of bounds ({position[0]},{position[1]})")
        
    def _validate_queens(self) -> bool:
        'validates all placed queens and replaces asset with the appropriate one'
        all_valid = True
        for position in self.queens:
            queen = self._board[position[0]][position[1]]
            is_valid_queen = queen['value'] == 0

            if is_valid_queen:
                if queen['asset'] in (self._invalid_queen_asset, None):
                    self._board[position[0]][position[1]]['asset'] = self._valid_queen_asset

            else:
                self._board[position[0]][position[1]]['asset'] = self._invalid_queen_asset
                all_valid = False
        
        return all_valid