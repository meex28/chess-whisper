from app.backend.speech.speech_to_text import transcribe_audio_file
from app.levels.types import ScenarioStepType, ScenarioStepCallback, UserInputHandler, ScenarioStep
from app.service.scenario_flow.callbacks import assistant_unrecognized_input_callback
from app.service.session_state import get_level_state, add_chat_message
import streamlit as st

def build_scenario_step(
        type: ScenarioStepType,
        callbacks: list[ScenarioStepCallback] = [],
        handlers: list[UserInputHandler] = []
) -> ScenarioStep:
    # TODO: validation of passed callback/handlers based on type?
    return ScenarioStep(
        type=type,
        callbacks=callbacks,
        handlers=handlers
    )

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
        add_chat_message("user", voice_recognition.text)
        handle_user_input(voice_recognition.text)
    else:
        print("Speech recognition failed")
        assistant_unrecognized_input_callback()
        st.rerun()

def handle_user_input(user_input: str):
    level_state = get_level_state()
    print(f"Handling user input (current scenario step={level_state.scenario_step_index}): {user_input}")
    current_step = level_state.level.scenario.steps[level_state.scenario_step_index]
    handlers = current_step.handlers

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
