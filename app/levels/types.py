from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

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

class RecognisedMoveIncorrectReason(Enum):
    NOT_ENOUGH_INFO = "not_enough_info"
    PIECE_NOT_SELECTED = "piece_not_selected"
    MULTIPLE_PIECES_FOUND = "multiple_pieces_found"
    PIECE_TYPE_MISMATCH = "piece_type_mismatch"
    WRONG_PLAYER_PIECE = "wrong_player_piece"
    # TODO: more detailed reasons why move is illegal (like "bishop can move only on diagonal")
    ILLEGAL_MOVE = "illegal_move"

class RestCallbackReason(Enum):
    PLAYER_COMMAND_INPUT = "player_command_input"


@dataclass
class RecognisedMove:
    correct: bool
    reason: Optional[RecognisedMoveIncorrectReason] = None
    piece: Optional[chess.PieceType] = None
    chess_move: Optional[chess.Move] = None
