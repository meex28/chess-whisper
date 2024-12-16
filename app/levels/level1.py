from app.backend.chess_engine.board_transformations import build_reset_board_transformation
from app.backend.chess_engine.engine import board_from_fen
from app.levels.types import ScenarioStepType, Scenario, Level
from app.service.scenario_flow.callbacks import build_assistant_text_callback, build_board_transformation_callback, \
    build_go_to_next_step_callback
from app.service.scenario_flow.handlers import build_user_confirmation_handler
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
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations = [
                build_reset_board_transformation(new_board=board_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")),
            ])
        ],
    ),
    build_scenario_step(
        type=ScenarioStepType.USER_ACTION,
        handlers=[

        ]
    )
])

level_one = Level(
    id="1",
    name="Notacja szachowa",
    scenario=_scenario
)
