import chess

from app.backend.chess_engine.board_transformations import build_reset_board_transformation, \
    build_highlight_squares_board_transformation, build_move_board_transformation, build_turn_set_transformation
from app.backend.chess_engine.engine import board_from_fen, str_to_square
from app.backend.chess_engine.types import SquareFillColor
from app.levels.types import ScenarioStepType, Scenario, Level
from app.service.scenario_flow.callbacks.go_to_next_step import build_go_to_next_step_callback
from app.service.scenario_flow.callbacks.board_transformation import build_board_transformation_callback
from app.service.scenario_flow.callbacks.assistant_text import build_assistant_text_callback
from app.service.scenario_flow.handlers.user_confirmation import build_user_confirmation_handler
from app.service.scenario_flow.handlers.move_expected import build_user_move_expected_handler
from app.levels.scenario_builder import build_scenario_step

_steps = [
    """
    Witaj! Cieszę się, że chcesz nauczyć się gry w szachy. 
    Zanim zaczniemy, opowiem Ci, czym są szachy, jakie są ich podstawowe zasady 
    i dlaczego tak wiele osób na całym świecie uwielbia tę grę. 
    """,
    """
    Gotowy, aby dowiedzieć się, o co w tym wszystkim chodzi?
    """,
    "USER",
    """
    Szachy to strategiczna gra planszowa dla dwóch osób, 
    rozgrywana na kwadratowej planszy zwanej szachownicą. 
    Szachownica składa się z 64 pól, na przemian białych i czarnych (jasnych i ciemnych).
    """,
    """
    Każdy z graczy kontroluje zestaw 16 figur w swoim kolorze – białym lub czarnym. 
    Grający na zmianę wykonują swoje ruchy, próbując osiągnąć jeden główny cel: 
    zamatować króla przeciwnika, czyli umieścić go w sytuacji, w której nie będzie mógł uniknąć zbicia. 
    Na wyższych poziomach nauczysz się, jak działają poszczególne elementy gry..
    """,
    """
    Czy jesteś gotowy aby przejść do podstawowych zasad?
    """,
    "USER",
    """
    Rozpoczynanie gry: Grę zawsze rozpoczynają białe. Gracze wykonują ruchy na zmianę.
    """,
    """
    Ruch figur: Każda figura porusza się w określony sposób.
    """,
    """
    Bicie: Gdy Twoja figura stanie na polu zajmowanym przez figurę przeciwnika, zbija ją i zajmuje jej miejsce.
    """,
    """
    Ochrona króla: Nigdy nie możesz wykonać ruchu, który narazi Twojego króla na bicie (szach).
    """,
    """
    Dodatkowo, w naszej aplikacji podczas trwania poziomu masz możliwość wykonania następujących akcji:
    ruchu, resetu poziomu, prośby o powtórzenie
    """,
    """
    Czy jesteś gotowy aby przejść do pierwszej praktycznej lekcji gry?            
    """,
    "USER",
]

_scenario: Scenario = Scenario(steps=[
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION if step == "USER" else ScenarioStepType.ASSISTANT_TEXT,
        handlers=[
            build_user_confirmation_handler(
                callbacks=[
                    build_go_to_next_step_callback()
                ]
            )
        ] if step == "USER" else None,
        callbacks=[
            build_assistant_text_callback(step),
            build_go_to_next_step_callback()
        ] if step != "USER" else None
    )
    for step in _steps
])

level_zero = Level(
    id="0",
    name="O co chodzi w szachach?",
    scenario=_scenario
)
