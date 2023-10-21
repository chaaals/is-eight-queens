from pathlib import Path

class EightQueens():
    """
    !REMOVE THIS!
    structure:
        1. properties first
        2. public methods next
        3. private methods last
    """

    def __init__(self, size: int = 8):
        self._size = size
        self._queen_positions = []
        self._board = [[{}]]
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
    
    def add_queen(self, position: tuple[int,int]):
        self._validate_position(position)
        self._queen_positions.append(position)
    
    def place_queen(self, position: tuple):
        self._validate_position(position)

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