from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

import chess


class UserActionType(Enum):
    MOVE = "move",

@dataclass
class Move:
    piece: chess.PieceType
    from_square: chess.Square
    to_square: chess.Square

@dataclass
class UserAction:
    type: UserActionType
    details: any # how to handle this?

UserActionHandler = Callable[
    [UserAction],
    [str]
]

@dataclass
class DialogStep:
    board: str # in FEN notation
    assistantText: str
    expectedUserAction: UserAction
    unexpectedUserActionHandler: UserActionHandler

@dataclass
class Level:
    name: str

