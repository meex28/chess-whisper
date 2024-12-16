from app.levels.types import ScenarioStepType, ScenarioStepCallback, UserInputHandler, ScenarioStep
from app.service.session_state import get_level_state


def build_scenario_step(
        type: ScenarioStepType,
        callbacks: list[ScenarioStepCallback] = [],
        handlers: list[UserInputHandler] = []
) -> ScenarioStep:
    # TODO: validation of passed callback/handlers based on type?
    return ScenarioStep(
        type=type,
        callbacks=callbacks,
        handlers=handlers
    )

def run_scenario_step():
    level_state = get_level_state()

    print(level_state)

    print(f"Running scenario step index: {level_state.scenario_step_index}")

    current_step = level_state.level.scenario.steps[level_state.scenario_step_index]

    for i, callback in enumerate(current_step.callbacks):
        print(f"Running callback index: {i}")
        callback()

def handle_user_input(user_input: str):
    print("Handling user input: ", user_input)
    level_state = get_level_state()
    handlers = level_state.level.scenario.steps[level_state.scenario_step_index].handlers
    for handler in handlers:
        result = handler(user_input, level_state)
        print(result)
