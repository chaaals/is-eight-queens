from pathlib import Path

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
    
    def place_queen(self, position: tuple):
        """
        Places a queen and their respective killzones on the board.
        Killzones can overlap and queens can be placed on killzones

        Args:
            position (tuple): row and column where the queen should be placed.
        Raises:
            ValueError: If the specified position is already occupied by another queen.
        """
        self._validate_position(position)
        row, column = position

        occupied = self._board[row][column]["id"] == "queen"
        if occupied:
            ALREADY_OCCUPIED = f"This tile ({row},{column}) already has a queen. It has {self._board[row][column]['id']} as the id\nDid you mean to use 'remove_queen()' instead?"
            raise ValueError(ALREADY_OCCUPIED)
        
        self._queen_positions.append(position)
        self._board[row][column]["id"] = "queen"

        def add_killzone(row: int, column: int):
            '''
            helper subfunction to add a killzone based on position given
            also checks if tile is empty beforehand to avoid replacing a queen's id with a killzone from other queens
            '''
            is_tile_empty = self._board[row][column]["id"] != "queen"
            if is_tile_empty:
                self._board[row][column]["id"] = "killzone"
                self._board[row][column]["asset"] = self._killzone_asset


        # row and column killzone
        for i in range(self.size):
            self._board[row][i]["value"] += 1

            # rows
            placed_queen = column
            if i != placed_queen:
                add_killzone(row, i)

            # columns
            placed_queen = row
            if i != placed_queen:
                add_killzone(i, column)
        
        # quadrant 1 (upper right)
        i=1
        while row-i>=0 and column+i<self.size:
            self._board[row-i][column+i]["value"] += 1
            add_killzone(row-i, column+i)
            i += 1

        # quadrant 2 (upper left)
        i=1
        while row-i>=0 and column-i>=0:
            self._board[row-i][column-i]["value"] += 1
            add_killzone(row-i, column-i)
            i += 1

        # quadrant 3 (bottom right)
        i=1
        while row+i<self.size and column-i>=0:
            self._board[row+i][column-i]["value"] += 1
            add_killzone(row+i, column-i)
            i += 1

        # quadrant 4 (bottom left)
        i=1
        while row+i<self.size and column+i<self.size:
            self._board[row+i][column+i]["value"] += 1
            add_killzone(row+i, column+i)
            i += 1

        self._validate_queens()

    def remove_queen(self, position: tuple):
        """
        Removes a queen and their respective killzones on the board.
        Removed killzones that overlapped with other killzones won't remove those other killzones

        Args:
            position (tuple): row and column of the queen to be removed.
        Raises:
            ValueError: If the specified position is not occupied by a queen.
        """
        self._validate_position(position)
        row, column = position
        
        occupied = self._board[row][column]["id"] == "queen"
        if not occupied:
            EMPTY_TILE = f"This tile ({row},{column}) does not have a queen. It has {self._board[row][column]['id']} as the id\nDid you mean to use 'place_queen()' instead?"
            raise ValueError(EMPTY_TILE)
        
        self._queen_positions.pop(self._queen_positions.index(position))

        self._board[row][column]["id"] = None

        removed_queen_was_killzone = self._board[row][column]["value"] > 0
        if removed_queen_was_killzone:
            self._board[row][column]["id"] = "killzone"

        def remove_killzone(row: int, column: int):
            '''
            helper subfunction to remove a killzone based on position given
            also to avoid replacing asset of an invalid queen when removing a killzone
            '''
            is_removed_killzone_empty = self._board[row][column]["value"] == 0 and self._board[row][column]["asset"] == self._killzone_asset
            if is_removed_killzone_empty:
                self._board[row][column]["id"] = None
                self._board[row][column]["asset"] = None

        # row and column killzone
        for i in range(self.size):
            self._board[row][i]["value"] -= 1

            # rows
            removed_queen = column
            if i != removed_queen:
                remove_killzone(row, i)

            # columns
            removed_queen = row
            if i != removed_queen:
                remove_killzone(i, column)
        
        # quadrant 1 (upper right)
        i=1
        while row-i>=0 and column+i<self.size:
            self._board[row-i][column+i]["value"] -= 1
            remove_killzone(row-i, column+i)
            i += 1

        # quadrant 2 (upper left)
        i=1
        while row-i>=0 and column-i>=0:
            self._board[row-i][column-i]["value"] -= 1
            remove_killzone(row-i, column-i)
            i += 1

        # quadrant 3 (bottom right)
        i=1
        while row+i<self.size and column-i>=0:
            self._board[row+i][column-i]["value"] -= 1
            remove_killzone(row+i, column-i)
            i += 1

        # quadrant 4 (bottom left)
        i=1
        while row+i<self.size and column+i<self.size:
            self._board[row+i][column+i]["value"] -= 1
            remove_killzone(row+i, column+i)
            i += 1

        self._validate_queens()

    def generate_answers(self):
        pass

    def export_board(self):
        pass

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
    
    def _validate_position(self, position: tuple[int,int]):
        'interrupt process if not a valid position'
        tuple_of_2_ints = (
            isinstance(position, tuple) and
            len(position) == 2 and
            all([isinstance(value, int) for value in position])
        )
        if not tuple_of_2_ints:
            raise ValueError("Position should be a tuple of 2 ints (position in x and y)")

        out_of_bounds = all(value > self.size for value in position)
        if out_of_bounds:
            raise ValueError(f"Position is out of bounds ({position[0]},{position[1]})")
        
    def _validate_queens(self):
        pass