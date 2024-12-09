import streamlit as st

from app.backend.chess_engine.engine import fen_board_to_svg
from app.levels.level1 import ScenarioEventType

def get_scenario_state():
    return st.session_state['scenario_state']

def go_to_next_scenario_step():
    get_scenario_state()['step_index'] += 1

def run_scenario_step():
    scenario_step_index = get_scenario_state()['step_index']
    scenario_step = st.session_state['scenario'][scenario_step_index]
    scenario_step_type = scenario_step[0]

    print(f"Running scenario step number {scenario_step_index}")

    if scenario_step_type == ScenarioEventType.ASSISTANT_TEXT:
        handle_assistant_text_step(scenario_step)
    elif scenario_step_type == ScenarioEventType.BOARD_UPDATE:
        handle_board_update_step(scenario_step)
    elif scenario_step_type == ScenarioEventType.USER_ACTION:
        pass

def handle_board_update_step(scenario_step):
    board_fen = scenario_step[1]['board_fen']
    board_path = fen_board_to_svg(
        fen=board_fen,
        highlighted_squares=scenario_step[1]['highlighted_squares']
    )
    get_scenario_state()['board_path'] = board_path
    print(f"Updated board to {board_path}")
    st.rerun()

def handle_assistant_text_step(scenario_step):
    # TODO: replace st.write with audio output
    st.write(scenario_step[1])
    go_to_next_scenario_step()
    run_scenario_step()

