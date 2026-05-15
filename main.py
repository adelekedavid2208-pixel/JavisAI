import os
from dotenv import load_dotenv
from groq import Groq

from voice import speak, record_audio
from router import parse_intent
from tools import open_app, web_search, get_time, get_date
from brain import ask_jarvis


# Load environment variables from .env
load_dotenv()

# Groq client for Whisper transcription
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------- SPEECH TO TEXT ----------------
def transcribe(file_path):
    try:
        with open(file_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=f,
                language="en"
            )

        return result.text.strip().lower()

    except Exception as e:
        print("Transcription error:", e)
        return ""


# ---------------- LISTEN FUNCTION ----------------
def listen():
    try:
        file_path = record_audio()
        return transcribe(file_path)

    except Exception as e:
        print("Listen error:", e)
        return ""


# ---------------- EXECUTE INTENT ----------------
def execute(intent):
    tool = intent.get("tool")

    if tool == "open_app":
        return open_app(intent.get("name", ""))

    if tool == "web_search":
        return web_search(intent.get("query", ""))

    if tool == "get_time":
        return f"The time is {get_time()}."

    if tool == "get_date":
        return f"Today is {get_date()}."

    # Default fallback
    return ask_jarvis(intent.get("input", ""))


# ---------------- MAIN LOOP ----------------
def main():
    print("Jarvis Phase 3 online.")
    speak("Jarvis phase three online and ready.")

    while True:
        command = listen()

        if not command:
            continue

        print("Heard:", command)

        # Exit command
        if "exit" in command or "stop" in command or "shutdown" in command:
            speak("Shutting down.")
            break

        # Wake word system
        if command.strip() == "jarvis":
            speak("Yes?")
            command = listen()
            print("Command:", command)

            if not command:
                continue

        # Parse intent using router
        try:
            intent = parse_intent(command)
            print("Intent:", intent)
        except Exception as e:
            print("Router error:", e)
            intent = {"tool": "chat", "input": command}

        # Execute
        try:
            response = execute(intent)
        except Exception as e:
            print("Execution error:", e)
            response = "Something went wrong while executing that."

        print("Jarvis:", response)
        speak(response)


if __name__ == "__main__":
    main()