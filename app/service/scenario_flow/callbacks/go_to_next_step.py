from app.levels.types import ScenarioStepCallback
from app.service.session_state import get_level_state


def go_to_next_step_callback():
    get_level_state().scenario_step_index += 1

def build_go_to_next_step_callback() -> ScenarioStepCallback:
    return lambda: go_to_next_step_callback()
