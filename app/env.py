import os
from dotenv import load_dotenv

load_dotenv()

AZURE_STT_API_KEY = os.getenv('AZURE_STT_API_KEY')
AZURE_TTS_API_KEY = os.getenv('AZURE_TTS_API_KEY')
AZURE_REGION = os.getenv('AZURE_REGION')
