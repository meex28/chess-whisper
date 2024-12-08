import chess
import chess.svg

from app.backend.chess_engine.types import SquareFillColor


def board_from_fen(fen: str) -> chess.Board:
    return chess.Board(fen)

def str_to_square(square: str) -> chess.Square:
    return chess.parse_square(square.lower())

def save_svg(svg: str, filename: str):
    with open(filename, 'w') as f:
        f.write(svg)

def board_to_svg(
        board: chess.Board,
        highlighted_squares: list[tuple[list[chess.Square], SquareFillColor]] = [],
        size: int =600,
        orientation: chess.Color =chess.WHITE
) -> str:
    fill_dict = {}

    for square_list, color in highlighted_squares:
        for square in square_list:
            fill_dict[square] = color.value

    return chess.svg.board(
        board=board,
        size=size,
        fill=fill_dict,
        coordinates=True,
        orientation=orientation
    )

# Example usage
def main():
    starting_fen = chess.STARTING_FEN
    board = board_from_fen(starting_fen)

    svg = board_to_svg(board, highlighted_squares=[
        ([str_to_square('d4'), str_to_square('d5')], SquareFillColor.RED),
        ([str_to_square('e4'), str_to_square('e5')], SquareFillColor.GREEN)
    ])
    save_svg(svg, 'sample_board.svg')

if __name__ == "__main__":
    main()
