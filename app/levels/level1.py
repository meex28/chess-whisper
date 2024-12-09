from app.backend.chess_engine.board_transformations import build_reset_board_transformation
from app.levels.types import ScenarioStepType, Scenario, Level, ScenarioStep
from app.service.scenario_flow.callbacks import build_assistant_text_callback, build_board_transformation_callback

_scenario: Scenario = Scenario(steps=[
    ScenarioStep(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Cześć! Jestem Twoim asystentem nauki szachów. 
            Za chwilę rozpoczniemy pierwszą lekcję, która nauczy Cię notacji szachowej. 
            Będzie ona kluczowe w sposobie, w jakim będziemy się porozumiewać. 
            Czy jesteś gotowy rozpocząć naszą pierwszą lekcję?
            """)
        ]
    ),
    ScenarioStep(
        type=ScenarioStepType.BOARD_TRANSFORMATION,
        callbacks=[
            build_board_transformation_callback(transformations = [
                build_reset_board_transformation(new_board_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"),
            ])
        ]
    ),
])

level_one = Level(
    id="1",
    name="Notacja szachowa",
    scenario=_scenario
)
