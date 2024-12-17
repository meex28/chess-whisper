import os

import streamlit as st
from audiorecorder import audiorecorder

from app.levels.level1 import level_one
from app.service.scenario_flow.scenario import run_scenario_step, handle_user_input, handle_user_input_from_voice
from app.service.session_state.session_state import init_session_state
from app.service.session_state.chat import get_chat_messages
from app.service.session_state.previous import save_previous_audio, get_previous_audio
from app.service.session_state.level_state import get_level_state

st.markdown(
    """
    <style>
        .chat-container {
            height: 500px;
            overflow-y: auto;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

init_session_state(level=level_one)

def board_component():
    board_path = get_level_state().board_svg_path
    with open(board_path, 'r') as f:
        svg = f.read()
    st.markdown(svg, unsafe_allow_html=True)

def audio_recorder_component():
    audio = audiorecorder("", "")
    if len(audio) > 0 and get_previous_audio() != audio:
        save_previous_audio(audio)
        
        try:
            os.makedirs("assets/user_input", exist_ok=True)
            audio.export("assets/user_input/voice.wav", format="wav")
            handle_user_input_from_voice("assets/user_input/voice.wav")
        except Exception as e:
            st.error(f"Error processing audio: {str(e)}")


st.title("Chess Whisper")
left_column, right_column = st.columns([1, 1])

with right_column:
    board_component()


with left_column:
    st.write("Current step index: ", get_level_state().scenario_step_index)

    with st.container(height=500):
        for message in get_chat_messages():
            if message["role"] == "assistant":
                st.chat_message("assistant").write(message["content"])
            else:
                st.chat_message("user").write(message["content"])

    if prompt := st.chat_input("Jaki jest twój ruch?"):
            handle_user_input(prompt)

    audio_recorder_component()

    if get_level_state().scenario_step_index > 0:
        run_scenario_step()

    if st.button("Start"):
        run_scenario_step()