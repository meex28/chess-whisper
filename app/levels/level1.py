from enum import Enum

from app.backend.chess_engine.engine import str_to_square
from app.backend.chess_engine.types import SquareFillColor
from app.levels.types import UserActionType


class ScenarioEventType(Enum):
    ASSISTANT_TEXT = "assistant_text",
    BOARD_UPDATE = "board_update",
    USER_ACTION = "user_action"

first_level_scenario = [
    (ScenarioEventType.ASSISTANT_TEXT,
     "Cześć! Jestem Twoim asystentem nauki szachów. Za chwilę rozpoczniemy pierwszą lekcję, która nauczy Cię notacji szachowej. Będzie ona kluczowe w sposobie, w jakim będziemy się porozumiewać. Czy jesteś gotowy rozpocząć naszą pierwszą lekcję?"
     ),
    (ScenarioEventType.BOARD_UPDATE, {
        "board_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
        "highlighted_squares": [
            ([str_to_square('d4'), str_to_square('d5')], SquareFillColor.RED),
            ([str_to_square('e4'), str_to_square('e5')], SquareFillColor.GREEN)
        ]
    }),
    (ScenarioEventType.USER_ACTION, {"type": UserActionType.CONFIRM})
]

