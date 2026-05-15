import os
import tempfile
import sounddevice as sd
import soundfile as sf
import numpy as np
import pyttsx3
from dotenv import load_dotenv

load_dotenv()

# --- SPEAK SYSTEM ---
def speak(text):
    print("Jarvis:", text)

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("TTS error:", e)


# --- RECORD AUDIO ---
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import queue
import time

SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 0.015
SILENCE_LIMIT = 1.2  # seconds of silence before stop


def record_audio():
    print("Listening... (smart mode)")

    audio_queue = queue.Queue()
    recording = []

    silence_start = None

    def callback(indata, frames, time_info, status):
        audio_queue.put(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback):
        while True:
            data = audio_queue.get()
            volume = np.linalg.norm(data) / len(data)

            recording.append(data)

            # detect speech
            if volume > SILENCE_THRESHOLD:
                silence_start = None
            else:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > SILENCE_LIMIT:
                    break

    audio = np.concatenate(recording, axis=0)

    # normalize
    audio = np.squeeze(audio)
    audio = audio / (np.max(np.abs(audio)) + 1e-6)

    file_path = tempfile.mktemp(suffix=".wav")
    sf.write(file_path, audio, SAMPLE_RATE)

    return file_path