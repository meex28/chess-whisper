import hashlib
import os

import azure.cognitiveservices.speech as speechsdk

from app.backend.speech.types import VoiceSynthesis
from app.env import AZURE_REGION, AZURE_TTS_API_KEY


def text_to_speech(text, output_file) -> VoiceSynthesis:
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_TTS_API_KEY, region=AZURE_REGION)
    speech_config.speech_synthesis_voice_name = "pl-PL-MarekNeural"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return VoiceSynthesis(success=True, output_path=output_file)
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Cannot synthesise speech: {}".format(result))
        return VoiceSynthesis(success=False, output_path="")

def get_audio_cache_filename(text, cache_dir='assets/voice_recordings'):
    os.makedirs(cache_dir, exist_ok=True)
    text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    cache_filename = os.path.join(cache_dir, f"{text_hash}.wav")
    return cache_filename

def get_speech_recording(text: str) -> VoiceSynthesis:
    cache_path = get_audio_cache_filename(text)
    if os.path.exists(cache_path):
        print(f"Using cached audio for text: {text}")
        return VoiceSynthesis(success=True, output_path=cache_path)

    return text_to_speech(text, cache_path)
