from app.levels.types import ScenarioStepType, ScenarioStepCallback, UserInputHandler, ScenarioStep


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
