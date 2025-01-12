import chess

from app.backend.chess_engine.board_transformations import (
    build_reset_board_transformation,
    build_highlight_squares_board_transformation,
)
from app.backend.chess_engine.engine import board_from_fen, str_to_square
from app.backend.chess_engine.types import SquareFillColor
from app.levels.types import ScenarioStepType, Scenario, Level
from app.service.scenario_flow.callbacks.go_to_next_step import build_go_to_next_step_callback
from app.service.scenario_flow.callbacks.board_transformation import build_board_transformation_callback
from app.service.scenario_flow.callbacks.assistant_text import build_assistant_text_callback
from app.service.scenario_flow.handlers.piece_placement_expected import build_user_piece_placement_expected_handler
from app.service.scenario_flow.handlers.user_confirmation import build_user_confirmation_handler
from app.levels.scenario_builder import build_scenario_step

_scenario: Scenario = Scenario(steps=[
    # Introduction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Witaj w drugiej lekcji! Dziś nauczysz się rozmieszczania głównych figur na szachownicy. 
            Poznasz ich początkowe pozycje, które są takie same w każdej grze szachowej. 
            Czy jesteś gotów?
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

    # Setup empty board
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=board_from_fen("8/8/8/8/8/8/8/8 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('a1')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Rook placement instruction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Świetnie! Skupimy się na rozmieszczeniu figur specjalnych. 
            Zaczniemy od białych na pierwszym rzędzie. Pierwsza figura po lewej stronie to wieża. 
            Zawsze ustawiamy ją na lewym, skrajnym polu pierwszego rzędu. Możesz ją tam umieścić?
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Rook placement action
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_piece_placement_expected_handler(
                expected_piece=chess.ROOK,
                expected_square=str_to_square('a1'),
                unexpected_move_text="Wieża powinna stanąć na polu A1. Spróbuj jeszcze raz.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/R7 w - - 0 1")),
                        build_highlight_squares_board_transformation(highlighted_squares=[
                            ([str_to_square('b1')], SquareFillColor.GREEN),
                        ])
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Knight instruction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Doskonale! Obok wieży, też w pierwszym rzędzie, ustawiamy skoczka.
            To figura, która porusza się w kształcie litery L. Umieść go teraz.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Knight placement
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_piece_placement_expected_handler(
                expected_piece=chess.KNIGHT,
                expected_square=str_to_square('b1'),
                unexpected_move_text="Skoczek powinien stanąć na polu B1, obok wieży. Spróbuj jeszcze raz.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/RN6 w - - 0 1")),
                        build_highlight_squares_board_transformation(highlighted_squares=[
                            ([str_to_square('c1')], SquareFillColor.GREEN),
                        ])
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Bishop instruction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Świetnie! Kolejna figura to goniec. On trafia na pole w kolumnie C.
            Goniec porusza się po skosie. Możesz go ustawić?
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Bishop placement
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_piece_placement_expected_handler(
                expected_piece=chess.BISHOP,
                expected_square=str_to_square('c1'),
                unexpected_move_text="Goniec powinien stanąć na polu C1. Spróbuj jeszcze raz.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/RNB5 w - - 0 1")),
                        build_highlight_squares_board_transformation(highlighted_squares=[
                            ([str_to_square('d1')], SquareFillColor.GREEN),
                        ])
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Queen instruction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Następna figura jest bardzo ważna - hetman. Jest to najsilniejsza figura na szachownicy.
            Ustawiamy ją zawsze na polu w tym samym kolorze co twoje bierki. Spróbuj.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Queen placement
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_piece_placement_expected_handler(
                expected_piece=chess.QUEEN,
                expected_square=str_to_square('d1'),
                unexpected_move_text="Hetman powinien stanąć na polu D1. Spróbuj jeszcze raz.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/RNBQ4 w - - 0 1")),
                        build_highlight_squares_board_transformation(highlighted_squares=[
                            ([str_to_square('e1')], SquareFillColor.GREEN),
                        ])
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # King instruction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Doskonale! Teraz najważniejsza figura - król. On zawsze staje na polu przeciwnego koloru. 
            To jedyna figura, którą musisz chronić za wszelką cenę. Postaw króla.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # King placement
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_piece_placement_expected_handler(
                expected_piece=chess.KING,
                expected_square=str_to_square('e1'),
                unexpected_move_text="Król powinien stanąć na polu E1. Spróbuj jeszcze raz.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/RNBQK3 w - - 0 1")),
                        build_highlight_squares_board_transformation(highlighted_squares=[
                            ([str_to_square('f1')], SquareFillColor.GREEN),
                        ])
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Rest pieces instruction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Świetnie! Teraz symetrycznie ustawimy pozostałe figury: gońca, skoczka i wieżę. Zacznij od lewej.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Second bishop placement
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_piece_placement_expected_handler(
                expected_piece=chess.BISHOP,
                expected_square=str_to_square('f1'),
                unexpected_move_text="Goniec powinien stanąć na polu F1. Spróbuj jeszcze raz.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/RNBQKB2 w - - 0 1")),
                        build_highlight_squares_board_transformation(highlighted_squares=[
                            ([str_to_square('g1')], SquareFillColor.GREEN),
                        ])
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Second knight placement
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_piece_placement_expected_handler(
                expected_piece=chess.KNIGHT,
                expected_square=str_to_square('g1'),
                unexpected_move_text="Skoczek powinien stanąć na polu g1. Spróbuj jeszcze raz.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/RNBQKBN1 w - - 0 1")),
                        build_highlight_squares_board_transformation(highlighted_squares=[
                            ([str_to_square('h1')], SquareFillColor.GREEN),
                        ])
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Second rook placement
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_piece_placement_expected_handler(
                expected_piece=chess.ROOK,
                expected_square=str_to_square('h1'),
                unexpected_move_text="Wieża powinna stanąć na polu H1. Spróbuj jeszcze raz.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/8/RNBQKBNR w - - 0 1")),
                        build_highlight_squares_board_transformation(highlighted_squares=[
                            ([str_to_square(s) for s in ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']], SquareFillColor.GREEN),
                        ])
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # Pawn instruction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Wszystkie pozostałe pionki to pionki na pierwszym rzędzie. Teraz je ustawimy.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Pawn placement
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations = [
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/8/8/PPPPPPPP/RNBQKBNR b - - 0 1")),
            ]),
            build_go_to_next_step_callback()
        ],
    ),

    # Opponent placement explanation
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Brawo! Wszystkie białe bierki są już na swoich pozycjach. 
            Czarna armia stoi po drugiej stronie planszy - symetrycznie do twoich figur. 
            Zwróć jedynie uwagę na króla i hetmana - one też stoją na polach odpowiedniego koloru.
            """),
            build_go_to_next_step_callback()
        ]
    ),
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations = [
                build_reset_board_transformation(new_board=chess.Board(fen=chess.STARTING_FEN)),
            ]),
            build_go_to_next_step_callback()
        ],
    ),

    # Final message
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Gratulacje! Nauczyłeś się rozmieszczać figury.
            W następnej lekcji nauczysz się, jak poruszają się poszczególne figury. Do zobaczenia!
            """),
            build_go_to_next_step_callback()
        ]
    ),
])

level_two = Level(
    id="2",
    name="Rozmieszczenie figur głównych",
    scenario=_scenario
)