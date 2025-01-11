from app.levels.types import Level
from app.service.session_state.chat import init_chat_state_if_empty, clear_chat_history
from app.service.session_state.level_state import init_level_state, init_level_state_if_empty
from app.service.session_state.playing_audio import init_playing_audio_state, reset_playing_audio_state
from app.service.session_state.previous import init_previous_if_empty
from app.service.session_state.processing_user_input import init_processing_user_input


def init_session_state(level: Level):
    init_level_state_if_empty(level=level)
    init_previous_if_empty()
    init_chat_state_if_empty()
    init_playing_audio_state()
    init_processing_user_input()

def reset_session_state(level: Level):
    init_level_state(level=level)
    init_previous_if_empty()
    clear_chat_history()
    reset_playing_audio_state()
    init_processing_user_input()
