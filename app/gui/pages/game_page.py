import streamlit as st
from audiorecorder import audiorecorder

from app.gui.scenario import run_scenario_step, get_scenario_state
from app.levels.level1 import first_level_scenario

if 'scenario_state' not in st.session_state:
    st.session_state['scenario_state'] = {
        'board_path': 'assets/starting_board.svg',
        'step_index': 0,
    }
st.session_state['scenario'] = first_level_scenario

def board_component():
    board_path = get_scenario_state()['board_path']
    with open(board_path, 'r') as f:
        svg = f.read()
    st.markdown(svg, unsafe_allow_html=True)

def audio_recorder_component():
    audio = audiorecorder("", "")
    if len(audio) > 0:
        audio.export("user_input.wav", format="wav")

st.title("Chess Whisper")
board_component()
audio_recorder_component()

if st.button("next scenario step"):
    run_scenario_step()