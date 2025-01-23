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
from app.service.scenario_flow.handlers.move_expected import build_user_move_expected_handler
from app.levels.scenario_builder import build_scenario_step

_scenario_checks: Scenario = Scenario(steps=[
    # Introduction to checks
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Witaj na poziomie o szachach i matach! Najważniejszym celem w szachach jest zamatowanie króla przeciwnika. 
            Zanim nauczysz się mata, poznaj pojęcie szacha - sytuacji, gdy twoja figura atakuje króla przeciwnika.
            """),
            build_go_to_next_step_callback()
        ],
    ),

    # First check demonstration
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="8/8/8/8/3K3r/8/8/8 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('h4')], SquareFillColor.RED),
                    ([str_to_square('d4')], SquareFillColor.YELLOW),
                    ([str_to_square('c5')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    # Check explanation
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Widzisz czerwone pole? Wieża atakuje króla, co oznacza szach. 
            Gdy jesteś w szachu, musisz natychmiast go zdjąć - przez ucieczkę, zasłonięcie lub zbicie atakującej figury.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # King escape instruction
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Spróbuj wydostać króla z szacha. Możesz go przesunąć na bezpieczne zielone pole.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # King escape move
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("d4c5"),
                unexpected_move_response="Spróbuj przesunąć króla na bezpieczne pole C5.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("d4c5")),
                        build_turn_set_transformation(color=chess.BLACK)
                    ]),
                    build_go_to_next_step_callback()
                ]
            )
        ]
    ),

    # User check scenario
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="rn3rk1/ppp1p1pp/8/1B6/6P1/P6P/1PPQP3/1K6 w - - 0 1")),
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Teraz wypróbujesz swoje nowe umiejętności w długim scenariuszu. Spójrz na sytuację na planszy.
            Zarówno Twój król jak i król przeciwnika nie są bezpieczni - stoją na otwartych pozycjach.
            Zobaczmy jaki ruch zrobi czarny.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_reset_board_transformation(new_board=chess.Board(fen="rn4k1/ppp1p1pp/8/1B6/6P1/P6P/1PPQP3/1K3r2 w - - 0 1")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('f1')], SquareFillColor.RED),
                    ([str_to_square('b1')], SquareFillColor.YELLOW),
                    ([str_to_square('a2')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Spójrz! Czarna wieża właśnie zaatakowała twojego króla. Masz aktualnie dwie opcje obrony.
            Pierwsza to zakrycie króla hetmanem ruchem na D1. Jest to jednak zły ruch, ponieważ wieża zbije go, znowu dając szacha.
            Druga opcja to ucieczka królem. Spróbuj ją wykonać na zielone pole.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # User king escape move
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("b1a2"),
                unexpected_move_response="Spróbuj przesunąć króla na bezpieczne pole A2.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("b1a2")),
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
            Teraz wieża nie zagraża już twojemu królowi. Poczekajmy na ruch czarnego.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_move_board_transformation(move=chess.Move.from_uci("a7a6")),
                build_turn_set_transformation(color=chess.WHITE),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('a6')], SquareFillColor.RED),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Czarny pion na polu A6 właśnie zaatakował twojego gońca. Jeśli nim nie uciekniesz to zostanie on zbity.
            Może to dobry moment, by wykorzystać go do ataku? Spróbuj dać nim szacha!
            """),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("b5c4"),
                unexpected_move_response="Spróbuj dać gońcem szacha po przekątnej, która będzie atakować czarnego króla.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("b5c4")),
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
            Świetnie! Czarny król musi się teraz bronić.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_move_board_transformation(move=chess.Move.from_uci("g8f8")),
                build_turn_set_transformation(color=chess.WHITE),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('f8')], SquareFillColor.YELLOW),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Czarny król właśnie uciekł na żółte pole F8 co pozwoli zaraz dać Ci mata.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Checkmate explanation
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Teraz poznasz mata - najważniejszy moment w szachach!
            Mat to sytuacja, gdy król jest w szachu i nie może się wydostać -
            nie ma wolnych pól, nie może być zasłonięty, a atakująca figura nie może być zbita.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations=[
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('d5')], SquareFillColor.RED),
                    ([str_to_square('e6')], SquareFillColor.RED),
                    ([str_to_square('f7')], SquareFillColor.RED),
                    ([str_to_square('g8')], SquareFillColor.RED),
                    ([str_to_square('d2')], SquareFillColor.YELLOW),
                    ([str_to_square('d8')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Twój goniec odcina już czarnemu królowi pola podświetlone na czerwono. 
            Nie może on na nie uciec ponieważ zaatakuje go twój goniec. Spójrz na swojego hetmana. 
            Jeśli trafi on na zielone pole to czarny król zostanie zamatowany. Spróbuj!
            """),
            build_go_to_next_step_callback()
        ]
    ),

    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("d2d8"),
                unexpected_move_response="Spróbuj dać mata hetmanem przesuwając go na zielone pole.",
                callbacks=[
                    build_board_transformation_callback(transformations=[
                        build_move_board_transformation(move=chess.Move.from_uci("d2d8")),
                        build_highlight_squares_board_transformation(highlighted_squares=[
                            ([str_to_square('d5')], SquareFillColor.RED),
                            ([str_to_square('e6')], SquareFillColor.RED),
                            ([str_to_square('f7')], SquareFillColor.RED),
                            ([str_to_square('g8')], SquareFillColor.RED),
                            ([str_to_square('e8')], SquareFillColor.RED),
                            ([str_to_square('f8')], SquareFillColor.RED),
                            ([str_to_square('h8')], SquareFillColor.RED),
                        ]),
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
            Doskonale! Właśnie wygrałeś tę partię, ponieważ zamatowałeś czarnego króla. 
            Wszystkie czerwone pola są atakowane, zatem nie ma on możliwości ucieczki ani zasłonięcia się.
            """),
            build_go_to_next_step_callback()
        ]
    ),

    # Conclusion
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Nauczyłeś się dwóch kluczowych pojęć w szachach: szacha i mata.
            Pamiętaj: w szachu musisz ratować króla, a w macie już nie ma ratunku!
            Do zobaczenia w następnej lekcji!
            """),
            build_go_to_next_step_callback()
        ]
    ),
])

level_checks = Level(
    id="9",
    name="Szachy i maty",
    scenario=_scenario_checks
)
