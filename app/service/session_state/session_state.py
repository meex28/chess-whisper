from dataclasses import dataclass
from typing import Literal
import streamlit as st

from app.levels.types import Level
from app.service.session_state.chat import init_chat_state_if_empty, clear_chat_history
from app.service.session_state.level_state import init_level_state, init_level_state_if_empty
from app.service.session_state.playing_audio import init_playing_audio_state, reset_playing_audio_state
from app.service.session_state.previous import init_previous_if_empty
from app.service.session_state.processing_user_input import init_processing_user_input

ScreenType = Literal["main_menu", "game"]

@dataclass
class SessionState:
    active_screen: ScreenType = "main_menu"

def init_session_state(level: Level):
    if "session_state" not in st.session_state:
        st.session_state.session_state = SessionState()
    
    init_level_state_if_empty(level=level)
    init_previous_if_empty()
    init_chat_state_if_empty()
    init_playing_audio_state()
    init_processing_user_input()
    if 'show_level_dialog' not in st.session_state:
        st.session_state.show_level_dialog = False

def reset_session_state(level: Level):
    st.session_state.session_state = SessionState()
    init_level_state(level)
    init_previous_if_empty()
    clear_chat_history()
    reset_playing_audio_state()
    init_processing_user_input()

def get_active_screen() -> ScreenType:
    return st.session_state.session_state.active_screen

def set_active_screen(screen: ScreenType):
    st.session_state.session_state.active_screen = screen

def set_show_level_dialog(show: bool):
    st.session_state.show_level_dialog = show

def get_show_level_dialog() -> bool:
    return st.session_state.get('show_level_dialog', False)
