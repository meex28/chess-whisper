import chess
import streamlit as st
from typing import List, Dict

from app.backend.chess_engine.engine import board_from_fen, save_svg, board_to_svg
from app.levels.types import Level, LevelState


def init_session_state(level: Level):
    init_level_state_if_empty(level=level)
    init_previous_if_empty()
    init_chat_state_if_empty()

def get_level_state() -> LevelState:
    return st.session_state['level_state']

def save_level_state(level_state: LevelState):
    st.session_state['level_state'] = level_state

def init_level_state(level: Level):
    start_board = board_from_fen(chess.STARTING_FEN)
    save_level_state(LevelState(
        level=level,
        scenario_step_index=0,
        user_color=chess.WHITE,
        board=start_board,
        board_svg_path=save_svg(board_to_svg(start_board), 'assets/starting_board.svg')
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

def init_chat_state_if_empty():
    if 'chat_messages' not in st.session_state:
        st.session_state['chat_messages'] = []

def add_chat_message(role: str, content: str):
    if 'chat_messages' not in st.session_state:
        init_chat_state_if_empty()
    
    st.session_state['chat_messages'].append({
        "role": role,
        "content": content
    })

def get_chat_messages() -> List[Dict[str, str]]:
    if 'chat_messages' not in st.session_state:
        init_chat_state_if_empty()
    return st.session_state['chat_messages']

def clear_chat_history():
    st.session_state['chat_messages'] = []

def reset_session_state():
    if 'level_state' in st.session_state:
        level = st.session_state['level_state'].level
        init_level_state(level)
