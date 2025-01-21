import chess

from app.backend.chess_engine.board_transformations import (
    build_reset_board_transformation,
    build_highlight_squares_board_transformation,
    build_move_board_transformation,
    build_turn_set_transformation
)
from app.backend.chess_engine.engine import str_to_square
from app.backend.chess_engine.types import SquareFillColor
from app.levels.types import ScenarioStepType, Scenario, Level
from app.service.scenario_flow.callbacks.go_to_next_step import build_go_to_next_step_callback
from app.service.scenario_flow.callbacks.board_transformation import build_board_transformation_callback
from app.service.scenario_flow.callbacks.assistant_text import build_assistant_text_callback
from app.service.scenario_flow.handlers.user_confirmation import build_user_confirmation_handler
from app.service.scenario_flow.handlers.move_expected import build_user_move_expected_handler
from app.levels.scenario_builder import build_scenario_step

_scenario: Scenario = Scenario(steps=[
    # Introduction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Witaj! Hetman (królowa) to najpotężniejsza figura w szachach. Może poruszać się jak wieża 
            (pionowo i poziomo) oraz jak goniec (po przekątnych) – na dowolną liczbę wolnych pól.
            """),
            build_go_to_next_step_callback()
        ],
    ),

    # Setup board for vertical move
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/3Q4 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('d1')], SquareFillColor.YELLOW),
                    ([str_to_square('d6')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Instruction for vertical move
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Hetman może poruszać się pionowo. Spróbuj przesunąć go na zielone pole.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Vertical move execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("d1d6"),
                unexpected_move_response="Spróbuj przesunąć hetmana z D1 na D6. Pamiętaj, że hetman porusza się jak wieża.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("d1d6")),
                        build_turn_set_transformation(color=chess.WHITE)
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Setup for diagonal move
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('d6')], SquareFillColor.YELLOW),
                    ([str_to_square('a3')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Instruction for diagonal move
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Hetman może poruszać się także po przekątnych, jak goniec. Spróbuj przesunąć go na zielone pole.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Diagonal move execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("d6a3"),
                unexpected_move_response="Spróbuj przesunąć hetmana z D6 na A3. Pamiętaj, że porusza się po przekątnych.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("d6a3")),
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
            Doskonale! Hetman to wszechstronna i bardzo potężna figura, dlatego często bywa kluczowa w partiach szachowych.
            Gratulacje! Opanowałeś jej podstawowe ruchy.
            """),
            build_go_to_next_step_callback()
        ]
    ),
])

level_six = Level(
    id="6",
    name="Ruchy hetmana",
    scenario=_scenario
)