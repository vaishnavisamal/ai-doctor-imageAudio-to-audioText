# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# Step1a: Setup Text to Speech - TTS - model with gTTS
import os
import asyncio
import subprocess
import platform

from gtts import gTTS
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)


def text_to_speech_with_gtts_old(input_text, output_filepath):
    language = "en"

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


# Step1b: Setup Text to Speech - TTS - model with edge-tts (FREE, no API key needed)
# pip install edge-tts
import edge_tts

# Some good default voices to try:
# "en-US-AriaNeural"   -> female, US English
# "en-US-GuyNeural"    -> male, US English
# "en-GB-SoniaNeural"  -> female, British English
# "en-IN-NeerjaNeural" -> female, Indian English
DEFAULT_VOICE = "en-US-AriaNeural"


async def _edge_tts_generate(input_text, output_filepath, voice=DEFAULT_VOICE):
    communicate = edge_tts.Communicate(input_text, voice)
    await communicate.save(output_filepath)


def text_to_speech_with_edge_tts_old(input_text, output_filepath, voice=DEFAULT_VOICE):
    asyncio.run(_edge_tts_generate(input_text, output_filepath, voice))


input_text = "Hi this is Ai with Vaishnavi!"
text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")
text_to_speech_with_edge_tts_old(input_text=input_text, output_filepath="edge_tts_testing.mp3")


# Step2: Use Model for Text output to Voice (with autoplay)

def _play_audio(output_filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":
            os.startfile(output_filepath)
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    _play_audio(output_filepath)


def text_to_speech_with_edge_tts(input_text, output_filepath, voice=DEFAULT_VOICE):
    asyncio.run(_edge_tts_generate(input_text, output_filepath, voice))
    _play_audio(output_filepath)


if __name__ == "__main__":
    input_text = "Hi this is Ai with Vaishnavi, autoplay testing!"

    # Uncomment whichever engine you want to test:
    # text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")
    text_to_speech_with_edge_tts(input_text=input_text, output_filepath="edge_tts_testing_autoplay.mp3")