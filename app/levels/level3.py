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
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/2R5/8/8/8/8 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('a5')], SquareFillColor.GREEN),
                    ([str_to_square('b5')], SquareFillColor.GREEN),
                    ([str_to_square('d5')], SquareFillColor.GREEN),
                    ([str_to_square('e5')], SquareFillColor.GREEN),
                    ([str_to_square('f5')], SquareFillColor.GREEN),
                    ([str_to_square('g5')], SquareFillColor.GREEN),
                    ([str_to_square('h5')], SquareFillColor.GREEN),

                    ([str_to_square('c1')], SquareFillColor.GREEN),
                    ([str_to_square('c2')], SquareFillColor.GREEN),
                    ([str_to_square('c3')], SquareFillColor.GREEN),
                    ([str_to_square('c4')], SquareFillColor.GREEN),
                    ([str_to_square('c6')], SquareFillColor.GREEN),
                    ([str_to_square('c7')], SquareFillColor.GREEN),
                    ([str_to_square('c8')], SquareFillColor.GREEN),
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
            Cześć! Dzisiaj poznasz ruchy wieży - jednej z najprostszych, ale też najsilniejszych, figur na szachownicy. 
            Jesteś gotów?
            """),
            build_go_to_next_step_callback()
        ],
    ),

    # User confirmation
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

    # Explanation of rook movement
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Wieża to figura, która porusza się prostoliniowo - w pionie i poziomie. 
            Wyobraź sobie, że wieża przemieszcza się jak żuraw na budowie - 
            prosto w górę, w dół, w lewo lub w prawo.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Setup board for vertical movement
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/R7 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('a1')], SquareFillColor.YELLOW),
                    ([str_to_square('a4')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Vertical movement instruction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Widzisz żółte pole z wieżą? Możesz ją przesunąć na zielone pole. Jak to zrobisz?
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Vertical movement execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("a1a4"),
                unexpected_move_response="Spróbuj przesunąć wieżę z A1 na A4. Pamiętaj, że wieża porusza się tylko w pionie i poziomie.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("a1a4")),
                        build_turn_set_transformation(color=chess.WHITE)
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Horizontal movement setup
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Dokładnie! Wieża może przechodzić przez wszystkie wolne pola w pionie.
            Teraz spróbuj przesunąć wieżę poziomo.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Highlight squares for horizontal movement
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('a4')], SquareFillColor.YELLOW),
                    ([str_to_square('d4')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Horizontal movement execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("a4d4"),
                unexpected_move_response="Spróbuj przesunąć wieżę z A4 na D4. Pamiętaj, że wieża porusza się tylko w pionie i poziomie.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("a4d4")),
                        build_turn_set_transformation(color=chess.WHITE)
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Setup capturing scenario
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/3R1n2/8/8/8 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('d4')], SquareFillColor.YELLOW),
                    ([str_to_square('f4')], SquareFillColor.RED),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Capturing instruction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Gdy wieża napotyka figurę przeciwnika, może ją zbić, zatrzymując się na jej polu. 
            Widzisz czerwone pole? Możesz spróbować wykonać zbicie.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Capture execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("d4f4"),
                unexpected_move_response="Spróbuj zbić figurę przeciwnika, przesuwając wieżę z D4 na F4.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("d4f4")),
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
            Widzisz, jak wieża jest potężna? Może kontrolować długie linie na szachownicy. 
            Ważna rada: staraj się umieszczać wieże na otwartych liniach, gdzie mają dużo wolnej przestrzeni do ruchu. 
            W następnej lekcji poznamy ruchy innej figury. Do zobaczenia!
            """),
            build_go_to_next_step_callback()
        ]
    ),
])

level_three = Level(
    id="3",
    name="Prosta, lecz potężna wieża",
    scenario=_scenario
)