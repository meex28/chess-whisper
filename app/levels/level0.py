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



_scenario_intro: Scenario = Scenario(steps=[
    # Introduction to chess
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Witaj! Cieszę się, że chcesz nauczyć się gry w szachy. 
            Zanim zaczniemy, opowiem Ci, czym są szachy, jakie są ich podstawowe zasady 
            i dlaczego tak wiele osób na całym świecie uwielbia tę grę.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Ready to learn?
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Gotowy, aby dowiedzieć się, o co w tym wszystkim chodzi?
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # User confirmation to continue
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_confirmation_handler(
                callbacks=[
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # What is chess?
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Szachy to strategiczna gra planszowa dla dwóch osób, 
            rozgrywana na kwadratowej planszy zwanej szachownicą. 
            Szachownica składa się z 64 pól, na przemian białych i czarnych (jasnych i ciemnych).
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Basic game description
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Każdy z graczy kontroluje zestaw 16 figur w swoim kolorze – białym lub czarnym. 
            Grający na zmianę wykonują swoje ruchy, próbując osiągnąć jeden główny cel: 
            zamatować króla przeciwnika, czyli umieścić go w sytuacji, w której nie będzie mógł uniknąć zbicia. 
            Na wyższych poziomach nauczysz się, jak działają poszczególne elementy gry.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Are you ready to learn the rules?
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Czy jesteś gotowy aby przejść do podstawowych zasad?
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # User confirmation to proceed to rules
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_confirmation_handler(
                callbacks=[
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Basic rules: starting the game
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Rozpoczynanie gry: Grę zawsze rozpoczynają białe. Gracze wykonują ruchy na zmianę.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Basic rules: piece movement
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Ruch figur: Każda figura porusza się w określony sposób.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Basic rules: capturing pieces
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Bicie: Gdy Twoja figura stanie na polu zajmowanym przez figurę przeciwnika, zbija ją i zajmuje jej miejsce.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Basic rules: protecting the king
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Ochrona króla: Nigdy nie możesz wykonać ruchu, który narazi Twojego króla na bicie (szach).
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Actions available in the application
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Dodatkowo, w naszej aplikacji podczas trwania poziomu masz możliwość wykonania następujących akcji:
            ruchu, resetu poziomu, prośby o powtórzenie.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Ready for the first practical lesson?
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Czy jesteś gotowy aby przejść do pierwszej praktycznej lekcji gry?
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # User confirmation to start practical lessons
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_confirmation_handler(
                callbacks=[
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),
])

level_zero = Level(
    id="0",
    name="O co chodzi w szachach?",
    scenario=_scenario_intro
)