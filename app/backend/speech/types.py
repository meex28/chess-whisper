from attr import dataclass

@dataclass
class VoiceRecognition:
    success: bool
    text: str

@dataclass
class VoiceSynthesis:
    success: bool
    output_path: str
