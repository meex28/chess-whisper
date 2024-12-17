from app.levels.types import ScenarioStepType, Scenario, Level
from app.service.scenario_flow.callbacks.assistant_text import build_assistant_text_callback
from app.levels.scenario_builder import build_scenario_step

_scenario: Scenario = Scenario(steps=[
    build_scenario_step(
        type=ScenarioStepType.ASSISTANT_TEXT,
        callbacks=[
            build_assistant_text_callback("""
            Cześć! To drugi poziom.
            """),
            # build_go_to_next_step_callback()
        ],
    ),
])

level_two = Level(
    id="2",
    name="Figury na planszy",
    scenario=_scenario
)
