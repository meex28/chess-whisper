import streamlit as st
from audiorecorder import audiorecorder

from app.levels.level1 import level_one
from app.service.scenario_flow.scenario import run_scenario_step, handle_user_input
from app.service.session_state import get_level_state, init_level_state_if_empty

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

st.write("Current step index: ", get_level_state().scenario_step_index)

user_input = st.text_input("user input")

if user_input:
    handle_user_input(user_input)

audio_recorder_component()

if get_level_state().scenario_step_index > 0:
    run_scenario_step()

if st.button("Start"):
    run_scenario_step()