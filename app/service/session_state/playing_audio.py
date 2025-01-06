from dataclasses import dataclass
from typing import Optional

import streamlit as st

key = 'playing_audio'

@dataclass
class PlayingAudioState:
    audio_file_path: Optional[str]
    is_playing: bool

def get_playing_audio_state() -> PlayingAudioState:
    return st.session_state[key]


def save_playing_audio_state(state: PlayingAudioState):
    st.session_state[key] = state


def reset_playing_audio_state():
    st.session_state[key] = PlayingAudioState(None, False)


def init_playing_audio_state():
    if key not in st.session_state:
        reset_playing_audio_state()