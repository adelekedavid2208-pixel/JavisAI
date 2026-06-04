import os
import time
import threading

from dotenv import load_dotenv
from groq import Groq

from voice import speak, record_audio
from router import parse_intent
from tools import open_app, web_search, get_time, get_date
from brain import ask_jarvis
from safety import is_safe
from memory import add_memory, get_memory

from realtime_core import text_queue, speech_queue


# =========================================
# LOAD ENVIRONMENT
# =========================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================================
# GLOBAL SPEAKING STATE (ADDED FIX)
# =========================================

is_speaking = False


# =========================================
# TRANSCRIPTION
# =========================================

def transcribe(file_path):

    if not file_path:
        return ""

    try:

        with open(file_path, "rb") as f:

            result = client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=f,
                language="en"
            )

        return result.text.strip().lower()

    except Exception as e:

        print("Transcription Error:", e)

        return ""


# =========================================
# EXECUTION ENGINE
# =========================================

def execute(plan):

    results = []

    if not isinstance(plan, list):
        plan = [plan]

    for step in plan:

        tool = step.get("tool")

        try:

            if tool == "open_app":
                results.append(
                    open_app(step.get("name", ""))
                )

            elif tool == "web_search":
                results.append(
                    web_search(step.get("query", ""))
                )

            elif tool == "get_time":
                results.append(
                    f"The time is {get_time()}."
                )

            elif tool == "get_date":
                results.append(
                    f"Today is {get_date()}."
                )

            elif tool == "memory":

                action = step.get("action", "")

                if action == "save":

                    text = step.get("text", "").strip()

                    if text:

                        add_memory(text)

                        results.append(
                            "Stored."
                        )

                    else:

                        results.append(
                            "Nothing to store."
                        )

                elif action == "recall":

                    query = step.get("query", "").lower()

                    memories = get_memory(limit=20)

                    found = None

                    for item in reversed(memories):

                        text = item.get("text", "")

                        if query in text.lower():

                            found = text
                            break

                    if found:

                        results.append(found)

                    else:

                        results.append(
                            "No matching memory found."
                        )

                else:

                    results.append(
                        "Memory action not recognized."
                    )

            elif tool == "chat":

                results.append(
                    ask_jarvis(
                        step.get("input", "")
                    )
                )

            else:

                results.append(
                    "Unknown command."
                )

        except Exception as e:

            print("Execution Error:", e)

            results.append(
                "Error executing command."
            )

    return " ".join(results)


# =========================================
# REAL-TIME LISTENER THREAD (FIXED)
# =========================================

def listener_loop():

    global is_speaking   # ADDED

    while True:

        # 🔒 BLOCK MIC WHILE SPEAKING
        if is_speaking:
            time.sleep(0.1)
            continue

        audio = record_audio()

        if not audio:
            continue

        text = transcribe(audio)

        if text:
            text_queue.put(text)


# =========================================
# REAL-TIME BRAIN THREAD
# =========================================

def brain_loop():

    wake_word = "jarvis"

    while True:

        command = text_queue.get()

        print("Heard:", command)

        if any(x in command for x in ["exit", "stop", "shutdown"]):

            speech_queue.put("Shutting down.")

            os._exit(0)

        if not is_safe(command):

            speech_queue.put(
                "Blocked for safety."
            )

            continue

        text = command

        if wake_word in text:

            text = text.replace(
                wake_word,
                ""
            ).strip()

            if not text:

                speech_queue.put("Yes?")
                continue

        command = text

        try:

            plan = parse_intent(command)

            print("Plan:", plan)

        except Exception as e:

            print("Router Error:", e)

            plan = [
                {
                    "tool": "chat",
                    "input": command
                }
            ]

        response = execute(plan)

        print("Jarvis:", response)

        speech_queue.put(response)


# =========================================
# SPEAKER THREAD (FIXED)
# =========================================

def speaker_loop():

    global is_speaking   # ADDED

    while True:

        text = speech_queue.get()

        is_speaking = True

        speak(text)

        is_speaking = False


# =========================================
# MAIN
# =========================================

def main():

    print("Jarvis Real-Time Mode Online.")

    speak(
        "Jarvis real time mode online and ready."
    )

    threading.Thread(
        target=listener_loop,
        daemon=True
    ).start()

    threading.Thread(
        target=brain_loop,
        daemon=True
    ).start()

    threading.Thread(
        target=speaker_loop,
        daemon=True
    ).start()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()