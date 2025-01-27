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

_scenario_king: Scenario = Scenario(steps=[
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/3K4/8/8/8/8 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('c4')], SquareFillColor.GREEN),
                    ([str_to_square('d4')], SquareFillColor.GREEN),
                    ([str_to_square('e4')], SquareFillColor.GREEN),
                    ([str_to_square('c5')], SquareFillColor.GREEN),
                    ([str_to_square('e5')], SquareFillColor.GREEN),
                    ([str_to_square('c6')], SquareFillColor.GREEN),
                    ([str_to_square('d6')], SquareFillColor.GREEN),
                    ([str_to_square('e6')], SquareFillColor.GREEN),
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
            Witaj! Dzisiaj nauczymy się ruchów króla. Król to najważniejsza figura w szachach. 
            Porusza się o jedno pole w dowolnym kierunku: pionowo, poziomo lub po przekątnych.
            """),
            build_go_to_next_step_callback()
        ],
    ),

    # Setup board for king's first move
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/4K3 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('e1')], SquareFillColor.YELLOW),
                    ([str_to_square('d2')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Instruction for moving king diagonally
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Król może poruszać się o jedno pole w dowolnym kierunku. Spróbuj przesunąć go na zielone pole.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Diagonal move execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("e1d2"),
                unexpected_move_response="Spróbuj przesunąć króla z E1 na D2. Pamiętaj, że król porusza się o jedno pole.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("e1d2")),
                        build_turn_set_transformation(color=chess.WHITE)
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Setup for horizontal move
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('d2')], SquareFillColor.YELLOW),
                    ([str_to_square('e2')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Instruction for horizontal move
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Świetnie! Teraz przesuwamy króla poziomo. Spróbuj przesunąć go na zielone pole.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Horizontal move execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("d2e2"),
                unexpected_move_response="Spróbuj przesunąć króla z D2 na E2. Pamiętaj, że król porusza się o jedno pole.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("d2e2")),
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
            Świetnie! Król jest kluczową figurą w szachach. Opanowanie jego ruchów jest bardzo ważne, 
            ponieważ to właśnie króla musisz chronić, aby wygrać partię.
            """),
            build_go_to_next_step_callback()
        ]
    ),
])

level_seven = Level(
    id="7",
    name="Ruchy króla",
    scenario=_scenario_king
)