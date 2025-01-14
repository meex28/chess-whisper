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

_scenario: Scenario = Scenario(steps=[
    # Introduction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Cześć! Dzisiaj nauczysz się ruchów gońca. Wiedziałeś, że w szachach każdy gracz ma dwóch gońców? 
            Na początku gry masz dwóch gońców: 
            jednego, który zawsze będzie się poruszał po białych polach i drugiego, który będzie się 
            przemieszczał tylko po czarnych polach. To bardzo ważna cecha gońców.
            """),
            build_go_to_next_step_callback()
        ],
    ),

    # Setup board for dark-squared bishop
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/2B2B2 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('c1')], SquareFillColor.YELLOW),
                    ([str_to_square('f4')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # First dark-squared bishop move instruction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Ten goniec może się poruszać tylko po czarnych polach. Widzisz zielone pole? 
            Spróbuj go tam przesunąć.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # First bishop move execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("c1f4"),
                unexpected_move_response="Spróbuj przesunąć gońca z C1 na F4. Pamiętaj, że goniec porusza się po skosie.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("c1f4")),
                        build_turn_set_transformation(color=chess.WHITE)
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Second move setup
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Dokładnie! Goniec przesuwa się wyłącznie po skosie, na dowolną liczbę wolnych pól.
            Teraz spróbuj przesunąć gońca na inną przekątną.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Highlight squares for second move
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('f4')], SquareFillColor.YELLOW),
                    ([str_to_square('c7')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Second move execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("f4c7"),
                unexpected_move_response="Spróbuj przesunąć gońca z F4 na C7. Pamiętaj, że goniec porusza się po skosie.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("f4c7")),
                        build_turn_set_transformation(color=chess.WHITE)
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Light-squared bishop introduction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Świetnie! Zauważ, że ten goniec zawsze będzie się poruszał po czarnych polach.
            Drugi goniec pozostanie zawsze na białych polach. Spróbuj go przesunąć.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Light-squared bishop setup
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('f1')], SquareFillColor.YELLOW),
                    ([str_to_square('c4')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Light-squared bishop move
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("f1c4"),
                unexpected_move_response="Spróbuj przesunąć gońca z F1 na C4. Pamiętaj, że goniec porusza się po skosie.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("f1c4")),
                        build_turn_set_transformation(color=chess.WHITE)
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Capturing setup
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/2B5/4n3/8/2B5/8/8/8 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('c4')], SquareFillColor.YELLOW),
                    ([str_to_square('e6')], SquareFillColor.RED),
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
            Gdy goniec napotyka figurę przeciwnika, może ją zbić, zatrzymując się na jej polu. 
            Widzisz czerwone pole? Możesz spróbować wykonać ruch zbicia.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Capture execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("c4e6"),
                unexpected_move_response="Spróbuj zbić figurę przeciwnika, przesuwając gońca z C4 na E6.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("c4e6")),
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
            Świetnie! Gońce są potężne, gdy mają dużo wolnej przestrzeni do ruchu po przekątnych. 
            Im więcej wolnych pól, tym są silniejsze. Widzę, że opanowałeś już podstawowe ruchy gońców. 
            Do zobaczenia w następnej lekcji!
            """),
            build_go_to_next_step_callback()
        ]
    ),
])

level_four = Level(
    id="4",
    name="Biały i czarny goniec",
    scenario=_scenario
)