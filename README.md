# Jarvis

A voice assistant for your Windows PC, inspired by Iron Man. Talk to it, and it answers out loud, opens your apps, searches Google, tells you the time, and remembers who you are.

> Early beta. Expect rough edges, and please tell me what breaks.

## What you need

- Windows 10 or 11
- Python 3.12 from python.org (tick "Add python.exe to PATH" and keep the `py` launcher option on when installing)
- A microphone and speakers
- A free Groq account, for the API key (https://console.groq.com)
- An internet connection (see "Privacy" and "Known limits")

## Quick start

1. Download or clone this project into a folder.
2. Double-click `run.bat`.
3. The first time, it creates its own environment and installs everything (a few minutes, a few hundred MB). It will then open a file called `.env`.
4. In `.env`, replace `paste-your-groq-key-here` with **your own** Groq key, save, close it, and double-click `run.bat` again.
5. Jarvis will ask what to call you. Say your name, then talk to it.

Your key stays on your computer in `.env`. Never share that file or upload it anywhere.

## Things to say

| Say | What happens |
|---|---|
| "What's the time?" / "What's the date?" | Answers instantly, even offline |
| "Open Chrome" / "Launch Spotify" | Opens an app installed on your PC |
| "Search Google for football news" | Opens the search in your browser |
| "Tell me about black holes" | Chats. Ask follow-ups like "tell me more" |
| "Remember that I like green tea" | Saves a fact about you |
| "Call me Sam" / "My name is Sam" | Changes the name it uses for you |
| "Forget this conversation" / "New topic" | Clears what it remembers of the current chat |
| "Exit" / "Stop" / "Shut down" | Closes Jarvis |

For detailed answers, ask in the same sentence: "explain black holes in detail".

## Memory and privacy

- Jarvis keeps its own memory for each person, in `%APPDATA%\Jarvis\memory.json` on your computer. It starts empty and learns only what you tell it. Nothing is shared between people or computers.
- It also remembers the last few exchanges while you talk (about 10 minutes). That part is never saved to disk.
- To erase everything it knows about you, close Jarvis and delete `%APPDATA%\Jarvis\memory.json`.
- **What you say is sent to Groq** (to turn speech into text and to write answers), along with your saved facts and the recent conversation. Don't tell Jarvis anything you wouldn't send to an online AI service.

## Settings (optional)

Add any of these to your `.env` file. The defaults work fine.

| Setting | Purpose |
|---|---|
| `GROQ_MODEL` | The Groq model used for answers |
| `GROQ_STT_MODEL` | The Groq model used to turn speech into text |
| `WHISPER_LOCAL_MODEL` | The offline model used when Groq can't be reached (default `base.en`) |
| `JARVIS_DATA_DIR` | A different folder for Jarvis's memory |

## Troubleshooting

- **"Access denied. Please check your network settings"** Groq is blocking your connection. Turn off any VPN or proxy and try again. Some networks and VPNs are blocked by Groq's protection.
- **It mishears me, or answers slowly after a network hiccup.** When Groq can't be reached, Jarvis falls back to a small offline model. It works, but it is slower and less accurate, especially on older or low-end computers.
- **It doesn't hear me.** Check that Windows is using the right microphone (Settings, System, Sound, Input), and that it isn't muted.
- **It hears itself or random noise.** Move the microphone away from the speakers, or use headphones.
- **A message about `.env` or the API key.** Make sure the file is named exactly `.env` (not `.env.txt`) and contains `GROQ_API_KEY=` followed by your key.
- **Apps don't open.** Jarvis finds apps through your Start menu. If an app isn't there, it can't open it yet.

## Known limits

- Windows only for now.
- Needs internet for answers and for good speech recognition.
- Only one person's memory per Windows login.
- It can mishear app names. If it opens the wrong one, just ask again.

## For developers

Run it by hand with `python main.py` inside the virtual environment. The `[timing]`, `[vad]`, `[stt]` and `[tts]` lines in the console show where time goes on each command.

Never commit `.env` or any `memory.json`. They are listed in `.gitignore`, and `.env.example` shows the expected format.
