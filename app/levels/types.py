from dataclasses import dataclass
from enum import Enum
from typing import Callable

import chess

ScenarioStepCallback = Callable[[], None]

class ScenarioStepType(Enum):
    ASSISTANT_TEXT = "assistant_text",
    BOARD_TRANSFORMATION = "board_transformation",
    USER_ACTION = "user_action"

@dataclass
class ScenarioStep:
    type: ScenarioStepType
    callbacks: list[ScenarioStepCallback]
    # TODO: add handlers

@dataclass
class Scenario:
    steps: list[ScenarioStep]

@dataclass
class Level:
    id: str
    name: str
    scenario: Scenario

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
