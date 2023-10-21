from pathlib import Path

class EightQueens():
    'description'

    def __init__(self, size: int = 8):
        self._size = size
        self._queen_positions = []
        self._board = [[{}]]
        """ temporary _generate_board for testing
        self._board = [[{
            "id": None,
            "value": 0,
            "asset": None
        } for _ in range(8)] for _ in range(8)]
        """
        self._valid_queen_asset = Path("path/to/valid/queen/asset")
        self._invalid_queen_asset = Path("path/to/invalid/queen/asset")
        self._killzone_asset = Path("path/to/killzone/asset")

        self._generate_board()
    
    @property
    def size(self) -> int:
        'return generated/updated board'
        return self._size

    @property
    def board(self) -> list[list[dict]]:
        'return generated/updated board'
        return self._board

    @property
    def queens(self) -> list[tuple[int,int]]:
        return self._queen_positions
    
    def place_queen(self, position: tuple):
        self._validate_position(position)
        self._queen_positions.append(position)

        row, column = position
        self._board[row][column]["id"] = "q"

        # row and column killzone
        for i in range(self.size):
            # rows
            placed_queen = column
            if i != placed_queen:
                self._board[row][i]["id"] = "k"
                self._board[row][i]["value"] += 1
                self._board[row][i]["asset"] = self._killzone_asset

            # columns
            placed_queen = row
            if i != placed_queen:
                self._board[i][column]["id"] = "k"
                self._board[i][column]["value"] += 1
                self._board[i][column]["asset"] = self._killzone_asset
        
        # quadrant 1 (upper right)
        i=1
        while row-i>=0 and column+i<self.size:
            self._board[row-i][column+i]["id"] = "k"
            self._board[row-i][column+i]["value"] += 1
            self._board[row-i][column+i]["asset"] = self._killzone_asset
            i += 1

        # quadrant 2 (upper left)
        i=1
        while row-i>=0 and column-i>=0:
            self._board[row-i][column-i]["id"] = "k"
            self._board[row-i][column-i]["value"] += 1
            self._board[row-i][column-i]["asset"] = self._killzone_asset
            i += 1

        # quadrant 3 (bottom right)
        i=1
        while row+i<self.size and column-i>=0:
            self._board[row+i][column-i]["id"] = "k"
            self._board[row+i][column-i]["value"] += 1
            self._board[row+i][column-i]["asset"] = self._killzone_asset
            i += 1

        # quadrant 4 (bottom left)
        i=1
        while row+i<self.size and column+i<self.size:
            self._board[row+i][column+i]["id"] = "k"
            self._board[row+i][column+i]["value"] += 1
            self._board[row+i][column+i]["asset"] = self._killzone_asset
            i += 1

        self._validate_queens()

    def remove_queen(self, position: tuple):
        self._validate_position(position)

    def generate_answers(self):
        pass

    def export_board(self):
        pass

    def file_to_board(self, file: Path):
        pass

    def _generate_board():
        'description'
        pass
    
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