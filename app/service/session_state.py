from dataclasses import dataclass

import chess
import streamlit as st

from app.levels.types import Level, LevelState


def get_level_state() -> LevelState:
    return st.session_state['level_state']

def save_level_state(level_state: LevelState):
    st.session_state['level_state'] = level_state

def init_level_state(level: Level):
    save_level_state(LevelState(
        level=level,
        scenario_step_index=0,
        board_fen=chess.STARTING_FEN,
        board_svg_path='assets/starting_board.svg'
    ))

def init_level_state_if_empty(level: Level):
    if 'level_state' not in st.session_state:
        init_level_state(level = level)