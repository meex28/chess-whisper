from app.levels.types import Level, ScenarioStepCallback
from app.service.session_state.session_state import reset_session_state

def build_select_level_callback(level: Level) -> ScenarioStepCallback:
    def run():
        reset_session_state(level=level)
    return run 