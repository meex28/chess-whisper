from app.levels.types import ScenarioStepCallback, UserInputHandler, LevelState, UserInputHandlerResult


def build_user_confirmation_handler(callbacks: list[ScenarioStepCallback]) -> UserInputHandler:
    def run(raw_user_input: str, _: LevelState) -> UserInputHandlerResult:
        confirmation_words = ["tak", "pewnie", "oczywiście", "jazda", "dawaj", "zaczynajmy"]
        user_input = raw_user_input.strip().lower()

        accepted = False
        for word in confirmation_words:
            if word in user_input:
                accepted = True
                break

        return UserInputHandlerResult(
            accepted=accepted,
            callbacks=callbacks if accepted else []
        )
    return run
