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

# puzzle from lichess: https://lichess.org/training/Sof8w

_scenario_puzzle_2: Scenario = Scenario(steps=[
    # Setup board for the puzzle
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="5qk1/ppp2p2/5Bp1/3P3Q/2r4r/6R1/P5P1/6K1 b - - 0 1")),
                build_turn_set_transformation(color=chess.WHITE)
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Introduction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            To druga, bardziej zaawansowana łamigłówka. Spróbuj przeanalizować aktualną pozycje.
            Tutaj możesz wygrać partię w trzech ruchach.
            """),
            build_go_to_next_step_callback()
        ],
    ),

    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("g3g6"),
                unexpected_move_response="Spróbuj znaleźć ruch, by zaatakować króla wieżą.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("g3g6")),
                        build_turn_set_transformation(color=chess.BLACK)
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            To dobry początek! Teraz czarny zaczyna obronę.
            """),
            build_go_to_next_step_callback()
        ],
    ),

    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_move_board_transformation(move=chess.Move.from_uci("f7g6")),
                build_turn_set_transformation(color=chess.WHITE),
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Jak kontynuujesz swój atak?
            """),
            build_go_to_next_step_callback()
        ],
    ),

    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("h5g6"),
                unexpected_move_response="Spróbuj wykonać podobny ruch jak ostatni ruch wieżą.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("h5g6")),
                        build_turn_set_transformation(color=chess.BLACK)
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Teraz czarnemu pozostaje jedynie rozpaczliwie się zasłonić!
            """),
            build_go_to_next_step_callback()
        ],
    ),

    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_move_board_transformation(move=chess.Move.from_uci("f8g7")),
                build_turn_set_transformation(color=chess.WHITE),
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Jak zakończysz tę partię?
            """),
            build_go_to_next_step_callback()
        ],
    ),

    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("g6g7"),
                unexpected_move_response="Musisz tak zaszachować króla by nie mógł uciec, zasłonić się lub zbić twojej figury.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("g6g7")),
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
            Świetnie! Udało Ci się rozwiązać całkiem skomplikowaną łamigłówkę. 
            Podczas prawdziwych partii zaczniesz z czasem zauważać takie schematy i wykorzystywać je do wygranych.
            """),
            build_go_to_next_step_callback()
        ]
    ),
])

level_puzzle_2 = Level(
    id="11",
    name="Druga łamigłówka",
    scenario=_scenario_puzzle_2
)