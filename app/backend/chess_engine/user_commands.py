from dataclasses import dataclass

import chess
import re
from typing import Optional

from app.levels.types import RecognisedMove, RecognisedMoveIncorrectReason


@dataclass
class RawMove:
    piece: Optional[chess.PieceType]
    fieldFrom: Optional[chess.Square]
    fieldTo: Optional[chess.Square]


def recognise_piece_from_move(text: str) -> Optional[chess.PieceType]:
    polish_pieces = {
        chess.KING: ['król', 'króla'],
        chess.QUEEN: ['królowa', 'królową', 'hetman', 'hetmana'],
        chess.ROOK: ['wieża', 'wieży', 'wieżą'],
        chess.BISHOP: ['goniec', 'gońca', 'gońcem'],
        chess.KNIGHT: ['skoczek', 'skoczkiem'],
        chess.PAWN: ['pion', 'pionem', 'piona', 'pionek', 'pionkiem', 'pionka']
    }

    piece_type = None
    for piece, names in polish_pieces.items():
        for name in names:
            if name in text:
                piece_type = piece
        if piece_type:
            break

    return piece_type

def recognise_squares_from_move(text: str) -> tuple[Optional[chess.Square], Optional[chess.Square]]:
    squares = []
    for column in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        for row in ['1', '2', '3', '4', '5', '6', '7', '8']:
            squares.append(column + row)

    square_pattern = r'[a-hA-H][1-8]'
    found_squares = re.findall(square_pattern, text)

    field_from: Optional[chess.Square] = None
    field_to: Optional[chess.Square] = None

    if len(found_squares) == 2:
        # If two squares are found, first is from, second is to
        field_from = chess.parse_square(found_squares[0])
        field_to = chess.parse_square(found_squares[1])
    elif len(found_squares) == 1:
        # If only one square is found, it's the destination
        field_to = chess.parse_square(found_squares[0])

    return field_from, field_to

def recognise_raw_move_from_text(raw_text: str) -> RawMove:
    text = raw_text.lower().strip()
    selected_piece = recognise_piece_from_move(text)
    selected_squares = recognise_squares_from_move(text)
    return RawMove(piece=selected_piece, fieldFrom=selected_squares[0], fieldTo=selected_squares[1])

def is_enough_move_info(raw_move: RawMove) -> bool:
    return raw_move.fieldTo is not None and (raw_move.fieldFrom is not None or raw_move.piece is not None)

def recognise_move_command(player_color: chess.Color, board: chess.Board, raw_text: str) -> RecognisedMove:
    raw_move = recognise_raw_move_from_text(raw_text)

    if not is_enough_move_info(raw_move):
        return RecognisedMove(
            correct=False,
            reason=RecognisedMoveIncorrectReason.NOT_ENOUGH_INFO
        )

    if raw_move.piece is None:
        piece = board.piece_at(raw_move.fieldFrom)
        if piece is None:
            return RecognisedMove(
                correct=False,
                reason=RecognisedMoveIncorrectReason.PIECE_NOT_SELECTED
            )
        raw_move.piece = piece.piece_type

    if raw_move.fieldFrom is None:
        pieces_on_board = board.pieces(piece_type=raw_move.piece, color=player_color)
        if len(pieces_on_board) == 0 or len(pieces_on_board) > 1:
            return RecognisedMove(
                correct=False,
                reason=RecognisedMoveIncorrectReason.MULTIPLE_PIECES_FOUND
            )
        raw_move.fieldFrom = list(pieces_on_board)[0]

    if board.piece_at(raw_move.fieldFrom).piece_type != raw_move.piece:
        return RecognisedMove(
            correct=False,
            reason=RecognisedMoveIncorrectReason.PIECE_TYPE_MISMATCH
        )

    if not board.piece_at(raw_move.fieldFrom).color == player_color:
        return RecognisedMove(
            correct=False,
            reason=RecognisedMoveIncorrectReason.WRONG_PLAYER_PIECE
        )

    chess_move = chess.Move(from_square=raw_move.fieldFrom, to_square=raw_move.fieldTo)
    if chess_move not in board.legal_moves:
        return RecognisedMove(
            correct=False,
            reason=RecognisedMoveIncorrectReason.ILLEGAL_MOVE
        )

    return RecognisedMove(
        correct=True,
        piece=raw_move.piece,
        chess_move=chess_move
    )
