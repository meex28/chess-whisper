from app.levels.types import UserInputHandlerResult, ScenarioStepCallback, UserInputHandler
from app.service.session_state import LevelState


def build_user_confirmation_handler(callbacks: list[ScenarioStepCallback]) -> UserInputHandler:
    def run(user_input: str, _: LevelState) -> UserInputHandlerResult:
        confirmation_words = ["tak", "pewnie", "oczywiście", "jazda", "dawaj"]
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
