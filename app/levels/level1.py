import chess

from app.backend.chess_engine.board_transformations import build_reset_board_transformation, \
    build_highlight_squares_board_transformation, build_move_board_transformation, build_turn_set_transformation
from app.backend.chess_engine.engine import board_from_fen, str_to_square
from app.backend.chess_engine.types import SquareFillColor
from app.levels.types import ScenarioStepType, Scenario, Level
from app.service.scenario_flow.callbacks import build_assistant_text_callback, build_board_transformation_callback, \
    build_go_to_next_step_callback
from app.service.scenario_flow.handlers import build_user_confirmation_handler, build_user_move_expected_handler
from app.service.scenario_flow.scenario import build_scenario_step

_scenario: Scenario = Scenario(steps=[
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Cześć! Jestem Twoim asystentem nauki szachów.
            Za chwilę rozpoczniemy pierwszą lekcję, która nauczy Cię notacji szachowej.
            Będzie ona kluczowa w sposobie, w jakim będziemy się porozumiewać.
            Czy jesteś gotowy na naszą pierwszą lekcję?
            """),
            build_go_to_next_step_callback()
        ],
    ),
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
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Notacja szachowa to prosty sposób opisywania ruchów. Każde pole na szachownicy ma swoją unikalną nazwę.
            Kolumny oznaczamy literami od A do H, idąc od lewej strony.
            Rzędy numerujemy od 1 do 8, od dolnej linii.
            Na przykład, pole w lewym dolnym rogu to A1, w centrum szachownicy to E4, a prawy górny róg to H8.
            Gdy chcesz wykonać ruch, powiedz mi dokładnie, skąd i dokąd przenosisz figurę.
            Możesz powiedzieć "skoczek z F3 na G5" albo "H1 na H7".
            """),
            build_go_to_next_step_callback()
        ],
    ),
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations = [
                build_reset_board_transformation(new_board=board_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")),
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('e2')], SquareFillColor.YELLOW),
                    ([str_to_square('e4')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ],
    ),
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("Sprawdźmy to w praktyce. Przesuń bierkę z żółtego pola na pole zielone."),
            build_go_to_next_step_callback()
        ]
    ),
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("e2e4"),
                unexpected_move_response="To nie jest ruch wskazany przez podświetlone pola. Sprawdź na którym rzędzie i w której kolumnie znajdują się pola, a następnie je wypowiedz, np. A1 na B2.",
                callbacks=[
                    build_board_transformation_callback(transformations = [
                        build_move_board_transformation(move=chess.Move.from_uci("e2e4")),
                        build_turn_set_transformation(color=chess.WHITE)
                    ]),
                    build_go_to_next_step_callback(),
                ]
            )
        ]
    ),
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("Dokładnie! Teraz zrób to w tej pozycji."),
            build_go_to_next_step_callback()
        ]
    ),
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations = [
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('f1')], SquareFillColor.YELLOW),
                    ([str_to_square('c4')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ],
    ),
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("f1c4"),
                unexpected_move_response="To nie jest ruch wskazany przez podświetlone pola. Sprawdź na którym rzędzie i w której kolumnie znajdują się pola, a następnie je wypowiedz, np. A1 na B2.",
                callbacks=[
                    build_board_transformation_callback(transformations = [
                        build_move_board_transformation(move=chess.Move.from_uci("f1c4")),
                        build_turn_set_transformation(color=chess.WHITE)
                    ]),
                    build_go_to_next_step_callback(),
                ]
            )
        ]
    ),
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("Tak! A teraz spróbujmy skoczkiem."),
            build_go_to_next_step_callback()
        ]
    ),
    build_scenario_step(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations = [
                build_highlight_squares_board_transformation(highlighted_squares=[
                    ([str_to_square('b1')], SquareFillColor.YELLOW),
                    ([str_to_square('c3')], SquareFillColor.GREEN),
                ])
            ]),
            build_go_to_next_step_callback()
        ],
    ),
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[
            build_user_move_expected_handler(
                expected_move=chess.Move.from_uci("b1c3"),
                unexpected_move_response="To nie jest ruch wskazany przez podświetlone pola. Sprawdź na którym rzędzie i w której kolumnie znajdują się pola, a następnie je wypowiedz, np. A1 na B2.",
                callbacks=[
                    build_board_transformation_callback(transformations = [
                        build_move_board_transformation(move=chess.Move.from_uci("b1c3")),
                        build_turn_set_transformation(color=chess.WHITE)
                    ]),
                    build_go_to_next_step_callback(),
                ]
            )
        ]
    ),
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("Myślę, że opanowałeś już tę lekcję. Możemy przejść do następnej."),
            build_go_to_next_step_callback()
        ]
    ),
])

level_one = Level(
    id="1",
    name="Notacja szachowa",
    scenario=_scenario
)
