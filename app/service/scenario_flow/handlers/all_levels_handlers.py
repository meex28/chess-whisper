from app.levels.types import LevelState, UserInputHandler, UserInputHandlerResult
from app.service.scenario_flow.callbacks import build_assistant_text_callback


def build_reset_level_command_handler() -> UserInputHandler:
    def run(user_input: str, _: LevelState) -> UserInputHandlerResult:
        reset_keywords = ["reset", "restart", "zacznij od nowa", "od początku"]
        accepted = any(keyword in user_input.lower() for keyword in reset_keywords)
        return UserInputHandlerResult(
            accepted=accepted,
            callbacks=[build_assistant_text_callback("Stan gry został zresetowany. Naciśnij przycisk Start aby rozpocząć ponownie.")]
        )
    return run

all_levels_handlers = [build_reset_level_command_handler()]