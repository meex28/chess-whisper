from app.backend.speech.speech_to_text import transcribe_audio_file


def handle_user_input(input_record_path):
    input_text = transcribe_audio_file(input_record_path).text
    print(input_text)
