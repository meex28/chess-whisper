import os

import streamlit as st
from audiorecorder import audiorecorder

from app.levels.level1 import level_one
from app.service.scenario_flow.scenario import run_scenario_step, handle_user_input, handle_user_input_from_voice
from app.service.session_state import get_level_state, save_previous_audio, \
    get_previous_audio, init_session_state

init_session_state(level=level_one)

def board_component():
    board_path = get_level_state().board_svg_path
    with open(board_path, 'r') as f:
        svg = f.read()
    st.markdown(svg, unsafe_allow_html=True)

def audio_recorder_component():
    audio = audiorecorder("", "")
    # TODO: handling is in endless loop when on re-renders
    if len(audio) > 0 and get_previous_audio() != audio:
        os.makedirs("assets/user_input", exist_ok=True)
        audio.export("assets/user_input/voice.wav", format="wav")
        handle_user_input_from_voice("assets/user_input/voice.wav")
        save_previous_audio(audio)

st.title("Chess Whisper")
board_component()

st.write("Current step index: ", get_level_state().scenario_step_index)

user_input = st.text_input("user input")

if st.button("Submit"):
    handle_user_input(user_input)
    user_input = None

audio_recorder_component()

if get_level_state().scenario_step_index > 0:
    run_scenario_step()

if st.button("Start"):
    run_scenario_step()