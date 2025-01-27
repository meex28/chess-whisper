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

_scenario_pawn: Scenario = Scenario(steps=[
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(
                    new_board=chess.Board(fen="rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('e5')], SquareFillColor.GREEN),
                    ([str_to_square('b3')], SquareFillColor.GREEN),
                    ([str_to_square('b4')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Introduction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Witaj! Dzisiaj nauczymy się ruchów pionka. Pionek porusza się do przodu o jedno pole, 
            ale tylko na początku może przesunąć się o dwa pola. Zbija figury, poruszając się po przekątnych.
            """),
            build_go_to_next_step_callback()
        ],
    ),

    # Setup for basic move
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/4P3/8 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('e2')], SquareFillColor.YELLOW),
                    ([str_to_square('e3')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Instruction for basic move
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Spróbuj przesunąć pionka o jedno pole do przodu na zielone pole.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Basic move execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("e2e3"),
                unexpected_move_response="Spróbuj przesunąć pionka z E2 na E3. Pionek porusza się o jedno pole do przodu.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("e2e3")),
                        build_turn_set_transformation(color=chess.WHITE)
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
            Doskonale! Pionek jest figurą, która może być kluczowa w końcowej fazie gry, 
            szczególnie gdy dotrze do końca szachownicy i może zostać promowany.
            """),
            build_go_to_next_step_callback()
        ]
    ),
])

level_eight = Level(
    id="8",
    name="Ruchy pionka",
    scenario=_scenario_pawn
)