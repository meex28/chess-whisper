from app.levels.all_levels import find_next_level
from app.levels.types import Level
from app.service.session_state.level_state import get_level_state, init_level_state


def build_go_to_next_level_callback(current_level: Level):
    def run():
        is_level_finished = get_level_state().scenario_step_index >= len(current_level.scenario.steps)
        next_level = find_next_level(get_level_state().level.id)
        if next_level is None or not is_level_finished:
            return
        init_level_state(level=next_level)
    return run
