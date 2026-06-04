import tempfile
import time
import queue

import numpy as np
import sounddevice as sd
import soundfile as sf
import pyttsx3

from realtime_core import is_speaking


# =====================================
# AUDIO SETTINGS
# =====================================

SAMPLE_RATE = 16000

# lower = more sensitive
SILENCE_THRESHOLD = 0.008

# faster cutoff
SILENCE_DURATION = 0.7

# shorter minimum speech
MIN_AUDIO_LENGTH = 0.6

# hard timeout
MAX_RECORD_TIME = 8


# =====================================
# SPEAK SYSTEM
# =====================================

def speak(text):
    """Reliable offline speech with mic lock"""

    text = str(text)

    print("Jarvis:", text)

    # =====================================
    # LOCK MICROPHONE
    # =====================================

    is_speaking.set()

    try:

        engine = pyttsx3.init()

        engine.setProperty("rate", 185)
        engine.setProperty("volume", 1.0)

        voices = engine.getProperty("voices")

        if voices:
            engine.setProperty(
                "voice",
                voices[0].id
            )

        engine.say(text)

        engine.runAndWait()

        engine.stop()

    except Exception as e:

        print("TTS Error:", e)

    finally:

        # tiny cooldown prevents echo pickup
        time.sleep(0.3)

        # =====================================
        # UNLOCK MICROPHONE
        # =====================================

        is_speaking.clear()


# =====================================
# REAL-TIME AUDIO RECORDER
# =====================================

def record_audio():

    # =====================================
    # DO NOT LISTEN WHILE SPEAKING
    # =====================================

    if is_speaking.is_set():
        time.sleep(0.1)
        return None

    audio_queue = queue.Queue()

    frames = []

    speech_started = False

    silence_start = None

    def callback(indata, frames_count, time_info, status):

        if status:
            print(status)

        audio_queue.put(indata.copy())

    try:

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=1024,
            callback=callback
        ):

            start_time = time.time()

            while True:

                # =====================================
                # STOP RECORDING IF JARVIS TALKS
                # =====================================

                if is_speaking.is_set():
                    return None

                try:

                    data = audio_queue.get(timeout=1)

                except queue.Empty:
                    continue

                volume = np.sqrt(np.mean(data**2))

                # speech detected
                if volume > SILENCE_THRESHOLD:

                    speech_started = True
                    silence_start = None

                # silence after speech
                elif speech_started:

                    if silence_start is None:

                        silence_start = time.time()

                    elif (
                        time.time() - silence_start
                        > SILENCE_DURATION
                    ):
                        break

                frames.append(data)

                # hard timeout
                if (
                    time.time() - start_time
                    > MAX_RECORD_TIME
                ):
                    break

    except Exception as e:

        print("Microphone Error:", e)

        return None

    if not frames:
        return None

    audio = np.concatenate(frames, axis=0)

    audio = np.squeeze(audio)

    duration = len(audio) / SAMPLE_RATE

    if duration < MIN_AUDIO_LENGTH:
        return None

    # normalize
    max_val = np.max(np.abs(audio))

    if max_val > 0:
        audio = audio / max_val

    temp_file = tempfile.mktemp(suffix=".wav")

    sf.write(
        temp_file,
        audio,
        SAMPLE_RATE
    )

    return temp_file