from app.backend.speech.text_to_speech import get_speech_recording
from app.service.session_state.chat import add_chat_message
from app.service.session_state.playing_audio import save_playing_audio_state, PlayingAudioState


def build_assistant_text_callback(text: str):
    # TODO: extract function, add loading state and keep conversation in session_state
    # TODO: wait until running next callback until text is finished
    def run():
        print(f"Playing assistant text: ${text}")
        voice_synthesis = get_speech_recording(text = text)

        if voice_synthesis.success:
            add_chat_message("assistant", text)
            save_playing_audio_state(PlayingAudioState(
                audio_file_path=voice_synthesis.output_path,
                is_playing=True
            ))
        else:
            print("Speech synthesis failed")
    return run

assistant_unrecognized_input_callback = build_assistant_text_callback(
    "Przepraszam ale nie zrozumiałem. Czy możesz powtórzyć swoją wypowiedź dokładniej?"
)
