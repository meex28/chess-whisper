import streamlit as st
from audiorecorder import audiorecorder

st.session_state['board_path'] = 'sample_board.svg'

def board_component():
    with open(st.session_state['board_path'], 'r') as f:
        svg = f.read()
    st.markdown(svg, unsafe_allow_html=True)

def audio_recorder_component():
    audio = audiorecorder("", "")
    if len(audio) > 0:
        audio.export("user_input.wav", format="wav")

st.title("Chess Whisper")
board_component()
audio_recorder_component()