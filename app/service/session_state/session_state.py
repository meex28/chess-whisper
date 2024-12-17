from app.levels.types import Level
from app.service.session_state.chat import init_chat_state_if_empty
from app.service.session_state.level_state import init_level_state, init_level_state_if_empty
from app.service.session_state.previous import init_previous_if_empty


def init_session_state(level: Level):
    init_level_state_if_empty(level=level)
    init_previous_if_empty()
    init_chat_state_if_empty()
