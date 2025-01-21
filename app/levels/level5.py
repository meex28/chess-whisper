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

_scenario_bishop: Scenario = Scenario(steps=[
    # Introduction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Witaj! Dzisiaj nauczysz się ruchów gońca. Goniec porusza się po przekątnych, 
            wyłącznie po polach w swoim kolorze – białych lub czarnych. Na początku każdy gracz 
            ma dwóch gońców: jednego na białych polach i jednego na czarnych.
            """),
            build_go_to_next_step_callback()
        ],
    ),

    # Setup board for dark-squared bishop
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/3B4 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('d1')], SquareFillColor.YELLOW),
                    ([str_to_square('h5')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Instruction for dark-squared bishop move
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Ten goniec porusza się wyłącznie po czarnych polach. Spróbuj przesunąć go na zielone pole.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Dark-squared bishop move execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("d1h5"),
                unexpected_move_response="Spróbuj przesunąć gońca z D1 na H5. Goniec porusza się po skosie.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("d1h5")),
                        build_turn_set_transformation(color=chess.WHITE)
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Setup board for light-squared bishop
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/4B3 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('e1')], SquareFillColor.YELLOW),
                    ([str_to_square('a5')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Instruction for light-squared bishop move
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Teraz spróbuj przesunąć drugiego gońca, który porusza się wyłącznie po białych polach. 
            Przesuń go na zielone pole.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Light-squared bishop move execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("e1a5"),
                unexpected_move_response="Spróbuj przesunąć gońca z E1 na A5. Goniec porusza się po skosie.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("e1a5")),
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
            Świetnie! Gońce są bardzo silne, gdy mają dużo przestrzeni do ruchu po przekątnych. 
            Pamiętaj, że zawsze pozostają na swoim kolorze pól. Gratulacje!
            """),
            build_go_to_next_step_callback()
        ]
    ),
])

level_five = Level(
    id="5",
    name="Ruchy gońca",
    scenario=_scenario_bishop
)