from dataclasses import dataclass
from enum import Enum
from typing import Callable

import chess

ScenarioStepCallback = Callable[[], None]

@dataclass
class UserInputHandlerResult:
    accepted: bool
    callbacks: list[ScenarioStepCallback]

UserInputHandler = Callable[[str, 'LevelState'], UserInputHandlerResult]

class ScenarioStepType(Enum):
    ASSISTANT_TEXT = "assistant_text",
    BOARD_TRANSFORMATION = "board_transformation",
    USER_ACTION = "user_action"

@dataclass
class ScenarioStep:
    type: ScenarioStepType
    callbacks: list[ScenarioStepCallback]
    handlers: list[UserInputHandler]

@dataclass
class Scenario:
    steps: list[ScenarioStep]

@dataclass
class Level:
    id: str
    name: str
    scenario: Scenario

@dataclass
class LevelState:
    level: Level
    scenario_step_index: int
    user_color: chess.Color
    board: chess.Board
    board_svg_path: str

@dataclass
class Move:
    piece: chess.PieceType
    from_square: chess.Square
    to_square: chess.Square
