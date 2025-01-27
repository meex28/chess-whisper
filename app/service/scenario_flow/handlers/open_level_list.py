from app.levels.types import UserInputHandler, LevelState, UserInputHandlerResult
from app.service.session_state.session_state import set_show_level_dialog

def build_open_level_list_handler() -> UserInputHandler:
    def run(user_input: str, _: LevelState) -> UserInputHandlerResult:
        level_list_keywords = ["lista poziomów", "liste poziomów", "listę poziomów", "pokaż poziomy", "wyświetl poziomy"]
        matches_keyword = any(keyword in user_input.lower() for keyword in level_list_keywords)
        
        if not matches_keyword:
            return UserInputHandlerResult(accepted=False, callbacks=[])

        return UserInputHandlerResult(
            accepted=True,
            callbacks=[
                lambda: set_show_level_dialog(True)
            ]
        )

    return run
