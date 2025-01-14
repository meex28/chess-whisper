from dataclasses import dataclass

import chess
from typing import Optional

from app.levels.types import RecognisedMove, RecognisedMoveIncorrectReason


@dataclass
class RawMove:
    piece: Optional[chess.PieceType]
    fieldFrom: Optional[chess.Square]
    fieldTo: Optional[chess.Square]


def recognise_piece_from_move(text: str) -> Optional[chess.PieceType]:
    polish_pieces = {
        chess.KING: [
            # Standard with diacritics
            'król', 'króla', 'królowi', 'królem', 'królu',
            # Without diacritics
            'krol', 'krola', 'krolowi', 'krolem', 'krolu'
        ],
        chess.QUEEN: [
            # Królowa with diacritics
            'królowa', 'królowej', 'królową', 'królowo',
            # Without diacritics
            'krolowa', 'krolowej', 'krolowa', 'krolowo',
            # Hetman variants
            'hetman', 'hetmana', 'hetmanowi', 'hetmanem', 'hetmanie',
            # Regional/colloquial
            'dama', 'damy', 'damą', 'damie'
        ],
        chess.ROOK: [
            # Standard with diacritics
            'wieża', 'wieży', 'wieżę', 'wieżą', 'wieżo',
            # Without diacritics
            'wieza', 'wiezy', 'wieze', 'wieza', 'wiezo',
            # Regional/colloquial
            'wieżowiec', 'wiezowiec', 'wieżyczka', 'wiezyczka',
            'tura', 'tury', 'turą', 'turze'
        ],
        chess.BISHOP: [
            # Goniec variants with diacritics
            'goniec', 'gońca', 'gońcowi', 'gońcem', 'gońcu',
            # Without diacritics
            'goniec', 'gonca', 'goncowi', 'goncem', 'goncu',
            # Laufer variants
            'laufer', 'laufra', 'laufrowi', 'laufrem', 'laufrze',
            # Regional/colloquial
            'giermek', 'giermka', 'giermkiem',
            'biegacz', 'biegacza', 'biegaczem',
            'poslaniec', 'posłaniec'
        ],
        chess.KNIGHT: [
            # Skoczek variants
            'skoczek', 'skoczka', 'skoczkowi', 'skoczkiem', 'skoczku',
            # Koń variants with diacritics
            'koń', 'konia', 'koniowi', 'koniem', 'koniu',
            # Without diacritics
            'kon', 'konia', 'koniowi', 'koniem', 'koniu',
            # Diminutive forms
            'koniczek', 'koniczka', 'koniczkowi', 'koniczkiem', 'koniczku',
            # Regional/colloquial
            'rumak', 'rumaka', 'rumakiem',
            'springer', 'springera', 'springerem',
            'skakacz', 'skakacza', 'skakaczem'
        ],
        chess.PAWN: [
            # Pion variants
            'pion', 'piona', 'pionowi', 'pionem', 'pionie',
            # Pionek variants
            'pionek', 'pionka', 'pionkowi', 'pionkiem', 'pionku',
            # Regional/colloquial
            'pieszek', 'pieszka', 'pieszkiem',
            'szeregowiec', 'szeregowca', 'szeregowcem',
            'zolnierzyk', 'żołnierzyk'
        ]
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
    # Letter representations mapping (standard and spoken/written forms)
    letter_variants = {
        'a': ['a', 'ah'],
        'b': ['b', 'be'],
        'c': ['c', 'ce'],
        'd': ['d', 'de'],
        'e': ['e', 'eh'],
        'f': ['f', 'ef'],
        'g': ['g', 'gie'],
        'h': ['h', 'ha']
    }

    # Number representations mapping (digits and Polish names)
    number_variants = {
        '1': ['1', 'jeden'],
        '2': ['2', 'dwa'],
        '3': ['3', 'trzy'],
        '4': ['4', 'cztery'],
        '5': ['5', 'pięć', 'piec'],
        '6': ['6', 'sześć', 'szesc'],
        '7': ['7', 'siedem'],
        '8': ['8', 'osiem']
    }

    # Generate all possible combinations with optional space
    combinations = []
    for chess_letter, letter_vars in letter_variants.items():
        for number, number_vars in number_variants.items():
            for letter_var in letter_vars:
                for number_var in number_vars:
                    # Add variant without space
                    combinations.append((f"{letter_var}{number_var}", chess_letter + number))
                    # Add variant with space
                    combinations.append((f"{letter_var} {number_var}", chess_letter + number))

    combinations.append(("ewa", "e2"))
    combinations.append(("EWA", "e2"))

    # Sort combinations by length (longer patterns first to avoid partial matches)
    combinations.sort(key=lambda x: len(x[0]), reverse=True)

    # Find all matches in the text
    text = text.lower()
    found_squares = []

    # Create a copy of text to modify
    remaining_text = text

    while remaining_text:
        found_match = False
        for pattern, square in combinations:
            if pattern in remaining_text:
                found_squares.append(square)
                # Remove the matched part and everything before it to avoid re-matching
                start_idx = remaining_text.index(pattern)
                remaining_text = remaining_text[start_idx + len(pattern):]
                found_match = True
                break
        if not found_match:
            # If no match found, remove first character and continue
            remaining_text = remaining_text[1:]

    field_from: Optional[chess.Square] = None
    field_to: Optional[chess.Square] = None

    if len(found_squares) >= 2:
        # If two or more squares are found, use the first two
        field_from = chess.parse_square(found_squares[0])
        field_to = chess.parse_square(found_squares[1])
    elif len(found_squares) == 1:
        # If only one square is found, it's the destination
        field_to = chess.parse_square(found_squares[0])

    return field_from, field_to

def recognise_raw_move_from_text(raw_text: str) -> RawMove:
    text = (raw_text.lower()
            .strip()
            .replace('.', '')
            .replace(',', '')
            )
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
