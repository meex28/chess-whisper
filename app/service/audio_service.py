from pydub import AudioSegment

def get_audio_duration(file_path: str) -> float:
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000  # Duration in seconds
