from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

import chess

@dataclass
class Move:
    piece: chess.PieceType
    from_square: chess.Square
    to_square: chess.Square

class UserActionType(Enum):
    MOVE = "move",
    CONFIRM = "confirm"

@dataclass
class UserAction:
    type: UserActionType
    details: any # how to handle this?

UserActionHandler = Callable[
    [UserAction],
    [str]
]

