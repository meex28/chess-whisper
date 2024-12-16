from collections.abc import Callable

import chess
from attr import dataclass

from app.backend.chess_engine.engine import board_to_svg, board_from_fen
from app.backend.chess_engine.types import SquareFillColor


@dataclass
class BoardState:
    board: chess.Board
    board_svg: str

# chess.Board -> BoardState
BoardTransformation = Callable[[chess.Board], BoardState]

def build_reset_board_transformation(new_board: chess.Board) -> BoardTransformation:
    return lambda current_board_fen: BoardState(
        board=new_board,
        board_svg=board_to_svg(new_board)
    )

def build_highlight_squares_board_transformation(
        highlighted_squares: list[tuple[list[chess.Square], SquareFillColor]]
) -> BoardTransformation:
    return lambda current_board: BoardState(
        board=current_board,
        board_svg=board_to_svg(
            board = current_board,
            highlighted_squares=highlighted_squares
        )
    )

def build_move_board_transformation(move: chess.Move) -> BoardTransformation:
    def transformation(current_board: chess.Board) -> BoardState:
        current_board.push(move)
        return BoardState(
            board=current_board,
            board_svg=board_to_svg(board=current_board)
        )
    return transformation

def build_turn_set_transformation(color: chess.Color) -> BoardTransformation:
    def transformation(current_board: chess.Board) -> BoardState:
        current_board.turn = color
        return BoardState(
            board=current_board,
            board_svg=board_to_svg(board=current_board)
        )
    return transformation
