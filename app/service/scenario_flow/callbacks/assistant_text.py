from app.service.session_state import add_chat_message


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
