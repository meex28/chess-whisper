from collections.abc import Callable

import chess
from attr import dataclass

from app.backend.chess_engine.engine import board_to_svg, board_from_fen
from app.backend.chess_engine.types import SquareFillColor


@dataclass
class BoardState:
    board_fen: str
    board_svg: str

# board_fen -> BoardState
BoardTransformation = Callable[[str], BoardState]

def build_reset_board_transformation(new_board_fen: str) -> BoardTransformation:
    return lambda current_board_fen: BoardState(
        board_fen=new_board_fen,
        board_svg=board_to_svg(board_from_fen(new_board_fen))
    )

def build_highlight_squares_board_transformation(
        highlighted_squares: list[tuple[list[chess.Square], SquareFillColor]]
) -> BoardTransformation:
    return lambda current_board_fen: BoardState(
        board_fen=current_board_fen,
        board_svg=board_to_svg(
            board = board_from_fen(current_board_fen),
            highlighted_squares=highlighted_squares
        )
    )

def build_move_board_transformation(move: chess.Move) -> BoardTransformation:
    def transformation(current_board_fen: str) -> BoardState:
        current_board = board_from_fen(current_board_fen)
        current_board.push(move)
        return BoardState(
            board_fen=current_board.fen(),
            board_svg=board_to_svg(board=current_board)
        )
    return transformation
