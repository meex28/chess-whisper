from app.levels.all_levels import find_next_level
from app.levels.types import UserInputHandler, LevelState, UserInputHandlerResult
from app.service.scenario_flow.callbacks.assistant_text import build_assistant_text_callback
from app.service.scenario_flow.callbacks.game_finished_callback import build_game_finished_callback
from app.service.scenario_flow.callbacks.go_to_next_level import build_go_to_next_level_callback


def build_go_to_next_level_command_handler() -> UserInputHandler:
    def run(user_input: str, level_state: LevelState) -> UserInputHandlerResult:
        keywords = ["dalej", "następny poziom"]
        is_level_finished = level_state.scenario_step_index >= len(level_state.level.scenario.steps)
        accepted = any(keyword in user_input.lower() for keyword in keywords) and is_level_finished

        if not accepted:
            return UserInputHandlerResult(
                accepted=False,
                callbacks=[]
            )

        next_level = find_next_level(level_state.level.id)
        if next_level is None:
            return UserInputHandlerResult(
                accepted=True,
                callbacks=[
                    build_game_finished_callback(),
                    build_assistant_text_callback("""
                    Brawo! Udało Ci się ukończyć wszystkie lekcje!
                    Teraz nadszedł czas na grę z prawdziwymi przeciwnikami. Powodzenia!
                    """)
                ]
            )

        return UserInputHandlerResult(
            accepted=True,
            callbacks=[build_go_to_next_level_callback(current_level=level_state.level)]
        )
    return run
