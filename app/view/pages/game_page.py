import asyncio
import os

import streamlit as st
from audiorecorder import audiorecorder
import sounddevice as sd

from app.levels.all_levels import all_levels
from app.service.audio_service import get_audio_duration
from app.service.scenario_flow.scenario import run_scenario_step, handle_user_input, handle_user_input_from_voice
from app.service.session_state.playing_audio import get_playing_audio_state, reset_playing_audio_state
from app.service.session_state.session_state import init_session_state, reset_session_state
from app.service.session_state.chat import get_chat_messages
from app.service.session_state.previous import save_previous_audio, get_previous_audio
from app.service.session_state.level_state import get_level_state, set_game_finished
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
            img {
                aspect-ratio: 1 / 1;
                object-fit: cover;
                border-radius: 8px;
            }
            [aria-label="dialog"] {
                width: 1500px;
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
        output_device = st.session_state.get('audio_output_device', None)
        if output_device is not None:
            try:
                sd.default.device[1] = output_device
            except Exception as e:
                print(f"Error setting output device: {e}")

        duration = get_audio_duration(audio_state.audio_file_path)
        st.audio(audio_state.audio_file_path, autoplay=True)
        asyncio.run(wait_and_run_callback(duration, on_audio_play_end))

def audio_recorder_component():
    input_device = st.session_state.get('audio_input_device', None)
    audio = audiorecorder("", "", key=f"audio_recorder_{input_device}")
    
    if len(audio) > 0 and get_previous_audio() != audio:
        save_previous_audio(audio)
        with st.spinner('Przetwarzam nagranie...'):
            try:
                os.makedirs("assets/user_input", exist_ok=True)
                print(f"Recording length: {len(audio)} samples")
                print(f"Recording sample rate: {audio.frame_rate}")

                audio.export("assets/user_input/voice.wav", format="wav")

                file_size = os.path.getsize("assets/user_input/voice.wav")
                print(f"Saved audio file size: {file_size} bytes")
                
                if file_size > 0:
                    handle_user_input_from_voice("assets/user_input/voice.wav")
                else:
                    st.error("Nagranie jest puste. Sprawdź ustawienia mikrofonu.")
            except Exception as e:
                st.error(f"Error processing audio: {str(e)}")
                print(f"Audio recording error: {str(e)}")

def user_interaction_component():
    can_user_interact = not get_playing_audio_state().is_playing
    has_level_started = get_level_state().scenario_step_index > 0
    has_level_ended = get_level_state().scenario_step_index >= len(get_level_state().level.scenario.steps)

    with st.container():
        if not has_level_started:
            if st.button("Start", use_container_width=True):
                reset_session_state(level=get_level_state().level)
                run_scenario_step()
            st.empty()
        elif not can_user_interact:
            if st.button("Pomiń audio", use_container_width=True):
                on_audio_play_end()
            st.empty()
        elif has_level_ended:
            if st.button("Następny poziom",use_container_width=True):
                handle_user_input("dalej")
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


def level_card(level):
    with st.container(border=True):
        image_path = f"assets/images/level{level.id}.png"
        if not os.path.exists(image_path):
            image_path = f"assets/images/level0.png"
        st.image(image_path, use_container_width=True)
        st.markdown(f"##### {level.id} - {level.name}")
        if st.button("Start", key=f"start_level_{level.id}", use_container_width=True):
            reset_session_state(level=level)
            st.rerun()

@st.dialog("Wybierz poziom", width="large")
def level_selection_dialog():
    columns = st.columns(5)

    for i, level in enumerate(all_levels):
        with columns[i % 5]:
            level_card(level)

def balloons_component():
    if get_level_state().game_finished:
        st.balloons()
        set_game_finished(is_finished=False)
    else:
        st.empty()

def sidebar_component():
    with st.sidebar:
        if st.button("Wybierz poziom", use_container_width=True):
            level_selection_dialog()

        st.markdown("---")
        if st.button("Reset poziomu", use_container_width=True):
            reset_session_state(level=get_level_state().level)
            run_scenario_step()
            st.rerun()
            
        st.markdown("---")
        
        # Audio settings
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        output_devices = [d for d in devices if d['max_output_channels'] > 0]
        
        if input_devices or output_devices:
            st.subheader("Ustawienia audio")
            
            if input_devices:
                input_device_names = [f"{i}: {d['name']}" for i, d in enumerate(input_devices)]
                selected_input = st.selectbox(
                    "Wejście audio",
                    input_device_names,
                    index=0
                )
                input_idx = int(selected_input.split(':')[0])
                st.session_state['audio_input_device'] = input_idx
            
            if output_devices:
                output_device_names = [f"{i}: {d['name']}" for i, d in enumerate(output_devices)]
                selected_output = st.selectbox(
                    "Wyjście audio",
                    output_device_names,
                    index=0
                )
                output_idx = int(selected_output.split(':')[0])
                st.session_state['audio_output_device'] = output_idx
                try:
                    sd.default.device[1] = output_idx
                except Exception as e:
                    print(f"Error setting output device: {e}")

def main():
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    init_session_state(level=all_levels[0])

    if get_level_state().scenario_step_index > 0 and not get_playing_audio_state().is_playing:
        run_scenario_step()

    page_styles()
    sidebar_component()
    page_header()
    page_body()

    balloons_component()

    play_audio_component()

if __name__ == "__main__":
    main()
