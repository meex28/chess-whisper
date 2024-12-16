import chess
import streamlit as st

from app.backend.chess_engine.engine import board_from_fen
from app.levels.types import Level, LevelState


def init_session_state(level: Level):
    init_level_state_if_empty(level=level)
    init_previous_if_empty()

def get_level_state() -> LevelState:
    return st.session_state['level_state']

def save_level_state(level_state: LevelState):
    st.session_state['level_state'] = level_state

def init_level_state(level: Level):
    save_level_state(LevelState(
        level=level,
        scenario_step_index=0,
        user_color=chess.WHITE,
        board=board_from_fen(chess.STARTING_FEN),
        board_svg_path='assets/starting_board.svg'
    ))

def init_level_state_if_empty(level: Level):
    if 'level_state' not in st.session_state:
        init_level_state(level = level)

def init_previous_if_empty():
    if 'previous' not in st.session_state:
        st.session_state['previous'] = {}
        st.session_state['previous']['audio'] = None

def save_previous_audio(audio):
    st.session_state['previous']['audio'] = audio

def get_previous_audio():
    return st.session_state['previous']['audio']
