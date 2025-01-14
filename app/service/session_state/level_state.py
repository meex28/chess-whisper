import chess
import streamlit as st

from app.backend.chess_engine.engine import board_from_fen, save_svg, board_to_svg
from app.levels.types import LevelState, Level
from app.service.session_state.chat import clear_chat_history


def get_level_state() -> LevelState:
    return st.session_state['level_state']


def save_level_state(level_state: LevelState):
    st.session_state['level_state'] = level_state


def set_game_finished(is_finished: bool):
    level_state = get_level_state()
    level_state.game_finished = is_finished
    save_level_state(level_state)


def init_level_state(level: Level):
    start_board = board_from_fen(chess.STARTING_FEN)
    save_level_state(LevelState(
        level=level,
        scenario_step_index=0,
        user_color=chess.WHITE,
        board=start_board,
        board_svg_path=save_svg(board_to_svg(start_board), 'assets/starting_board.svg')
    ))
    clear_chat_history()


def init_level_state_if_empty(level: Level):
    if 'level_state' not in st.session_state:
        init_level_state(level = level)
