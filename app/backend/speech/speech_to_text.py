import azure.cognitiveservices.speech as speechsdk

from app.backend.speech.types import VoiceRecognition, VoiceRecognitionResult
from app.env import AZURE_STT_API_KEY, AZURE_REGION


def transcribe_audio_file(audio_file_path) -> VoiceRecognition:
    speech_config = speechsdk.SpeechConfig(
        subscription=AZURE_STT_API_KEY,
        region=AZURE_REGION,
        speech_recognition_language="pl-PL"
    )
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return VoiceRecognition(success=True, text=result.text)
    else:
        return VoiceRecognition(success=False, text="")
