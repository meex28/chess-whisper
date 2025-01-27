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

_scenario_knight: Scenario = Scenario(steps=[
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/4N3/8/8/8/8 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('d7')], SquareFillColor.GREEN),
                    ([str_to_square('f7')], SquareFillColor.GREEN),
                    ([str_to_square('c6')], SquareFillColor.GREEN),
                    ([str_to_square('g6')], SquareFillColor.GREEN),
                    ([str_to_square('c4')], SquareFillColor.GREEN),
                    ([str_to_square('g4')], SquareFillColor.GREEN),
                    ([str_to_square('d3')], SquareFillColor.GREEN),
                    ([str_to_square('f3')], SquareFillColor.GREEN),
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
            Cześć! Dzisiaj nauczysz się ruchów konia. Wiedziałeś, że koń porusza się w nietypowy sposób? 
            Wykonuje ruch w kształcie litery „L” – dwa pola w jednym kierunku i jedno w innym, 
            lub jedno pole w jednym kierunku i dwa w innym. Koń to jedyna figura, która może przeskakiwać inne figury!
            """),
            build_go_to_next_step_callback()
        ],
    ),

    # Setup board for knight's first move
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/4N3 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('e1')], SquareFillColor.YELLOW),
                    ([str_to_square('g2')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # First knight move instruction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Koń porusza się w kształcie litery „L”. Widzisz zielone pole? 
            Spróbuj przesunąć tam konia.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # First knight move execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("e1g2"),
                unexpected_move_response="Spróbuj przesunąć konia z E1 na G2. Pamiętaj o ruchu w kształcie litery „L”.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("e1g2")),
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
            Świetnie! Koń może poruszać się na osiem różnych pól, o ile są w zasięgu jego ruchu „L”. 
            Spróbuj przesunąć konia na inne zielone pole.
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
                    ([str_to_square('g2')], SquareFillColor.YELLOW),
                    ([str_to_square('f4')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Second knight move execution
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("g2f4"),
                unexpected_move_response="Spróbuj przesunąć konia z G2 na F4. Pamiętaj o ruchu w kształcie litery „L”.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("g2f4")),
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
            Brawo! Koń to wyjątkowa figura, ponieważ potrafi przeskakiwać inne figury i zawsze porusza się w kształcie litery „L”. 
            Opanowanie ruchów konia pozwala na tworzenie zaskakujących zagrożeń w partii. Do zobaczenia w następnej lekcji!
            """),
            build_go_to_next_step_callback()
        ]
    ),
])

level_four = Level(
    id="4",
    name="Ruchy konia",
    scenario=_scenario_knight
)