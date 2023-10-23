from algorithm.eight_queens import EightQueens

def main() -> None:
    x = EightQueens()

    # print("_"*10,"add queen 0,0")
    # x.place_queen(0,0)
    # print_board(x, "value")
    
    # print("_"*10,"add queen 1,1")
    # x.place_queen(1,1)
    # print_board(x, "value")

    # print("_"*10,"add queen 1,2")
    # x.place_queen(1,2)
    # print_board(x, "value")

    # print("_"*10,"remove queen 1,1")
    # x.remove_queen(1,1)
    # print_board(x, "value")

    x.generate_answers()
    print_board(x, "id")
    x.file_to_board()  # Use the default './boards' directory
#     print_imported_boards(x)

    total_boards = len(x.imported_boards)
    total_dictionaries = sum(len(row) * len(tile) for board in x.imported_boards for row in board for tile in row)

    for board in x.imported_boards:
        for row in board:
            for tile in row:
                if tile['id'] == "queen":
                    print("Q", end="\t")
                elif tile['id'] == "killzone":
                    print(".", end="\t")
                else:
                    print("!", end="\t")
                print({
                    "id": tile["id"],
                    "value": tile["value"],
                    "asset": tile["asset"]
                })
            print()  # Print a newline after each row
        print("new Board")  # Print "new Board" to separate boards

    print(f"Total boards created: {total_boards}")
    print(f"Total dictionaries created: {total_dictionaries}")


def print_board(board: EightQueens, data: str = "id"):
    for row in board.board:
        for value in row:
            print(value[data],end="\t")
        print()

if __name__ == "__main__":
    main()