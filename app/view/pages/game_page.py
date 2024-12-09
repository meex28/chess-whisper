import streamlit as st
from audiorecorder import audiorecorder

from app.levels.level1 import level_one
from app.service.scenario_flow.scenario import run_scenario_step
from app.service.session_state import init_level_state_if_empty, get_level_state

init_level_state_if_empty(level = level_one)

def board_component():
    board_path = get_level_state().board_svg_path
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