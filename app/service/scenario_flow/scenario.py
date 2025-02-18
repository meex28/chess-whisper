from app.backend.speech.speech_to_text import transcribe_audio_file
from app.levels.types import ScenarioStepType
from app.service.scenario_flow.all_levels_handlers import all_levels_handlers
from app.service.scenario_flow.callbacks.assistant_text import assistant_unrecognized_input_callback
from app.service.scenario_flow.handlers.go_to_next_level import build_go_to_next_level_command_handler
from app.service.scenario_flow.handlers.reset_level import build_reset_level_command_handler
from app.service.session_state.chat import add_chat_message
from app.service.session_state.level_state import get_level_state
from app.service.scenario_flow.handlers.select_another_level import build_select_level_command_handler
from app.service.scenario_flow.handlers.open_level_list import build_open_level_list_handler
import streamlit as st


def run_scenario_step():
    level_state = get_level_state()

    if level_state.scenario_step_index >= len(level_state.level.scenario.steps):
        return

    print(f"Running scenario step index: {level_state.scenario_step_index}")
    print(f"Current level state: {level_state}")

    current_step = level_state.level.scenario.steps[level_state.scenario_step_index]

    if current_step.type == ScenarioStepType.USER_ACTION:
        return

    for i, callback in enumerate(current_step.callbacks):
        print(f"Running callback index: {i}")
        callback()

    st.rerun()

def handle_user_input_from_voice(recording_path: str):
    voice_recognition = transcribe_audio_file(recording_path)

    if voice_recognition.success:
        handle_user_input(voice_recognition.text)
    else:
        print("Speech recognition failed")
        assistant_unrecognized_input_callback()
        st.rerun()

def handle_user_input(user_input: str):
    level_state = get_level_state()
    print(f"Handling user input (current scenario step={level_state.scenario_step_index}): {user_input}")

    add_chat_message("user", user_input)

    current_step = level_state.level.scenario.steps[level_state.scenario_step_index] if level_state.scenario_step_index < len(level_state.level.scenario.steps) else None
    handlers = all_levels_handlers + (current_step.handlers if current_step else []) + [
        build_select_level_command_handler(),
        build_reset_level_command_handler(),
        build_go_to_next_level_command_handler(),
    ]
    if handlers is None or len(handlers) == 0:
        return

    # run results from first accepted handler
    all_handlers_result = None
    for handler in handlers:
        result = handler(user_input, level_state)
        if result.accepted:
            all_handlers_result = result
            break

    if all_handlers_result is not None:
        for i, callback in enumerate(all_handlers_result.callbacks):
            print(f"Running user input callback index: {i}")
            callback()
    else:
        assistant_unrecognized_input_callback()

    st.rerun()
