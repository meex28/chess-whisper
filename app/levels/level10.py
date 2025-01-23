import chess

from app.backend.chess_engine.board_transformations import (
    build_reset_board_transformation,
    build_highlight_squares_board_transformation,
    build_move_board_transformation,
    build_turn_set_transformation
)
from app.backend.chess_engine.engine import board_from_fen, str_to_square
from app.backend.chess_engine.types import SquareFillColor
from app.levels.types import ScenarioStepType, Scenario, Level
from app.service.scenario_flow.callbacks.go_to_next_step import build_go_to_next_step_callback
from app.service.scenario_flow.callbacks.board_transformation import build_board_transformation_callback
from app.service.scenario_flow.callbacks.assistant_text import build_assistant_text_callback
from app.service.scenario_flow.handlers.user_confirmation import build_user_confirmation_handler
from app.service.scenario_flow.handlers.move_expected import build_user_move_expected_handler
from app.levels.scenario_builder import build_scenario_step

_scenario_mate_in_one: Scenario = Scenario(steps=[
    # Introduction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Witaj! Twoim zadaniem jest dać mata przeciwnikowi w jednym posunięciu. Przyjrzyj się uważnie pozycji 
            i znajdź zwycięski ruch.
            """),
            build_go_to_next_step_callback()
        ],
    ),

    # Setup board for the puzzle
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="r5k1/1b4pr/4b1p1/p2pP1Q1/P2P4/2PB1N1P/5PP1/5RK1 b - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('g5')], SquareFillColor.YELLOW)
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Instruction for the user
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Zwróć uwagę na pozycję króla przeciwnika. Pamiętaj, że mat oznacza brak możliwości ucieczki dla króla. 
            Wykonaj ruch, który zakończy grę.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Execution of the winning move
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("g5h6"),
                unexpected_move_response="Spróbuj znaleźć ruch, który da mata. Przemyśl pozycję jeszcze raz.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("g5h6")),
                        build_turn_set_transformation(color=chess.BLACK)
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Conclusion
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Świetnie! To był mat w jednym ruchu. Gratulacje, udało Ci się rozwiązać tę łamigłówkę. 
            Pamiętaj, że zrozumienie takich pozycji pomoże Ci wygrywać partie w przyszłości.
            """),
            build_go_to_next_step_callback()
        ]
    ),
])

level_mate_in_one = Level(
    id="10",
    name="Łamigłówka",
    scenario=_scenario_mate_in_one
)