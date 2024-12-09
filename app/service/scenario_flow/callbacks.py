from io import BytesIO

from pydub import AudioSegment
from pydub.playback import play

from app.backend.chess_engine.board_transformations import BoardTransformation
from app.backend.speech.text_to_speech import get_speech_recording
from app.levels.types import ScenarioStepCallback
from app.service.session_state import get_level_state

def go_to_next_step_callback():
    get_level_state().scenario_step_index += 1

def build_go_to_next_step_callback() -> ScenarioStepCallback:
    return lambda: go_to_next_step_callback()

def build_board_transformation_callback(transformations: list[BoardTransformation]) -> ScenarioStepCallback:
    pass

def build_assistant_text_callback(text: str):
    # TODO: extract function, add loading state and keep conversation in session_state
    def run():
        print(f"Playing assistant text: ${text}")
        voice_synthesis = get_speech_recording(text = text)

        if voice_synthesis.success:
            audio_file = open(voice_synthesis.output_path, 'rb')
            audio_bytes = audio_file.read()
            # TODO: isn't quality of this audio too low?
            audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format='wav')
            play(audio_segment)
        else:
            print("Speech synthesis failed")
    return run