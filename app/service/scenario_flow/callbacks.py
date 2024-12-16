from io import BytesIO

from pydub import AudioSegment
from pydub.playback import play

from app.backend.chess_engine.board_transformations import BoardTransformation
from app.backend.chess_engine.engine import save_svg
from app.backend.speech.text_to_speech import get_speech_recording
from app.levels.types import ScenarioStepCallback
from app.service.session_state import get_level_state, save_level_state, add_chat_message


def go_to_next_step_callback():
    get_level_state().scenario_step_index += 1

def build_go_to_next_step_callback() -> ScenarioStepCallback:
    return lambda: go_to_next_step_callback()

def build_board_transformation_callback(transformations: list[BoardTransformation]) -> ScenarioStepCallback:
    def run():
        level_state = get_level_state()

        for transformation in transformations:
            result = transformation(level_state.board)
            level_state.board = result.board
            board_svg_path = 'assets/current_board.svg'
            save_svg(result.board_svg, board_svg_path)
            level_state.board_svg_path = board_svg_path

        save_level_state(level_state)
    return run

def build_assistant_text_callback(text: str):
    # TODO: extract function, add loading state and keep conversation in session_state
    # TODO: wait until running next callback until text is finished
    def run():
        # print(f"Playing assistant text: ${text}")
        # voice_synthesis = get_speech_recording(text = text)
        #
        # if voice_synthesis.success:
        #     audio_file = open(voice_synthesis.output_path, 'rb')
        #     audio_bytes = audio_file.read()
        #     # TODO: isn't quality of this audio too low?
        #     audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format='wav')
        #     play(audio_segment)
        # else:
        #     print("Speech synthesis failed")
        add_chat_message("assistant", text)
    return run

assistant_unrecognized_input_callback = build_assistant_text_callback(
    "Przepraszam ale nie zrozumiałem. Czy możesz powtórzyć swoją wypowiedź dokładniej?"
)
