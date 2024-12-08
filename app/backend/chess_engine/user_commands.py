from dataclasses import dataclass

import chess
import re
from typing import Optional

from app.levels.types import Move


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

def recognise_move_command(player_color: chess.Color, board: chess.Board, raw_text: str) -> Optional[Move]:
    raw_move = recognise_raw_move_from_text(raw_text)

    if not is_enough_move_info(raw_move):
        print("Not enough information to recognise a move")
        return None

    if raw_move.piece is None:
        piece = board.piece_at(raw_move.fieldFrom)
        if piece is None or piece.color != player_color:
            print("Player's piece was not selected")
            return None
        raw_move.piece = piece.piece_type

    if raw_move.fieldFrom is None:
        pieces_on_board = board.pieces(piece_type=raw_move.piece, color=player_color)
        if len(pieces_on_board) == 0 or len(pieces_on_board) > 1:
            print("There is no selected piece type on the board or there are more than one")
            return None
        raw_move.fieldFrom = list(pieces_on_board)[0]

    if board.piece_at(raw_move.fieldFrom).piece_type != raw_move.piece:
        print(f"Piece type at selected square is different than selected piece type (on board: {board.piece_at(raw_move.fieldFrom).piece_type}, selected: {raw_move.piece})")
        return None

    if not board.piece_at(raw_move.fieldFrom).color == player_color:
        print("Selected piece doesn't belong to the player")
        return None

    chess_move = chess.Move(from_square=raw_move.fieldFrom, to_square=raw_move.fieldTo)
    if chess_move not in board.legal_moves:
        print(f"Selected move is illegal (move: {chess_move}, legal moves: {list(board.legal_moves)})")
        return None

    return Move(
        piece=raw_move.piece,
        from_square=raw_move.fieldFrom,
        to_square=raw_move.fieldTo,
    )
