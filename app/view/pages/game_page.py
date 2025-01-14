import asyncio
import os

import streamlit as st
from audiorecorder import audiorecorder

from app.levels.all_levels import all_levels
from app.service.audio_service import get_audio_duration
from app.service.scenario_flow.scenario import run_scenario_step, handle_user_input, handle_user_input_from_voice
from app.service.session_state.playing_audio import get_playing_audio_state, reset_playing_audio_state
from app.service.session_state.session_state import init_session_state, reset_session_state
from app.service.session_state.chat import get_chat_messages
from app.service.session_state.previous import save_previous_audio, get_previous_audio
from app.service.session_state.level_state import get_level_state
from app.service.util import wait_and_run_callback

def page_styles():
    st.markdown(
        """
        <style>
            .chat-container {
                height: 500px;
                overflow-y: auto;
            }
            .stAudio {
                display: none;
            }
            .block-container {
                display: flex;
                align-items: center;
                justify-content: center;
                padding-top: 6rem;
                padding-left: 0rem;
                padding-right: 0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def board_component():
    board_path = get_level_state().board_svg_path
    with open(board_path, 'r') as f:
        svg = f.read()
    st.markdown(svg, unsafe_allow_html=True)

def on_audio_play_end():
    reset_playing_audio_state()
    st.rerun()

def play_audio_component():
    audio_state = get_playing_audio_state()
    if audio_state.is_playing and audio_state.audio_file_path:
        duration = get_audio_duration(audio_state.audio_file_path)
        st.audio(audio_state.audio_file_path, autoplay=True)
        asyncio.run(wait_and_run_callback(duration, on_audio_play_end))

def audio_recorder_component():
    audio = audiorecorder("", "")
    if len(audio) > 0 and get_previous_audio() != audio:
        save_previous_audio(audio)
        with st.spinner('Przetwarzam nagranie...'):
            try:
                os.makedirs("assets/user_input", exist_ok=True)
                audio.export("assets/user_input/voice.wav", format="wav")
                handle_user_input_from_voice("assets/user_input/voice.wav")
            except Exception as e:
                st.error(f"Error processing audio: {str(e)}")

def user_interaction_component():
    can_user_interact = not get_playing_audio_state().is_playing
    has_level_started = get_level_state().scenario_step_index > 0
    has_level_ended = get_level_state().scenario_step_index >= len(get_level_state().level.scenario.steps)

    with st.container():
        if not has_level_started:
            if st.button("Start", use_container_width=True):
                reset_session_state(level=get_level_state().level)
                run_scenario_step()
            st.empty() # add empty to hide audio_recorder_component, IDK why it doesn't hide after rerender
        elif not can_user_interact:
            if st.button("Skip >>", use_container_width=True):
                on_audio_play_end()
            st.empty()
        elif has_level_ended:
            if st.button("Dalej", use_container_width=True):
                handle_user_input("dalej") # should go to next level
            st.empty()
        else:
            if prompt := st.chat_input(placeholder="Jaki jest twój ruch?"):
                handle_user_input(prompt)
            audio_recorder_component()

def chat_component():
    with st.container(height=500):
        for message in get_chat_messages():
            if message["role"] == "assistant":
                st.chat_message("assistant").write(message["content"])
            else:
                st.chat_message("user").write(message["content"])

    user_interaction_component()

def page_header():
    current_level = get_level_state().level

    st.title(f'Poziom {current_level.id}: {current_level.name}')

def page_body():
    left_column, right_column = st.columns([1, 1])
    with right_column:
        board_component()
    with left_column:
        chat_component()

def sidebar_component():
    with st.sidebar:
        st.title("Wybór poziomu")
        levels = all_levels
        
        for level in levels:
            if st.button(f"Poziom {level.id} - {level.name}", use_container_width=True):
                reset_session_state(level=level)
                st.rerun()

        st.markdown("---")  # horizontal line
        if st.button("Reset poziomu", use_container_width=True):
            reset_session_state(level=get_level_state().level)
            st.rerun()

def main():
    init_session_state(level=all_levels[0])
    if get_level_state().scenario_step_index > 0 and not get_playing_audio_state().is_playing:
        run_scenario_step()
    page_styles()
    sidebar_component()
    page_header()
    page_body()

    # put at the script end to not block the main thread
    play_audio_component()

if __name__ == "__main__":
    main()
