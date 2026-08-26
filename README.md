# Jarvis AI

> A real-time voice AI assistant for Windows inspired by Iron Man's Jarvis.

Jarvis is an AI desktop assistant capable of listening, understanding, remembering, and responding to voice commands in real time. It combines speech recognition, an AI planner, long-term memory, and voice responses into a natural conversational experience.

**This project is currently in active development.**

---

## Features

- Real-time voice interaction
- AI-powered conversation
- Long-term memory
- Natural text-to-speech responses
- Date and time queries
- Web search
- Open Windows applications
- Basic safety filtering
- Multi-threaded architecture for smooth interaction

---

## Tech Stack

- Python
- Groq API
- Whisper (Speech-to-Text)
- pyttsx3
- sounddevice
- faster-whisper (experimental)
- JSON Memory Store

---

## Project Structure

```
JarvisAI/
│
├── main.py
├── router.py
├── brain.py
├── voice.py
├── tools.py
├── memory.py
├── safety.py
├── realtime_core.py
├── memory.json
└── README.md
```

---

## Current Capabilities

Jarvis can currently:

- Answer general questions
- Remember user information
- Recall saved memories
- Open Windows applications
- Search the web
- Tell the date and time
- Hold natural conversations

---

## Roadmap

### Version 0.2
- Better speech recognition
- Smarter application detection
- Improved conversational memory

### Version 0.3
- File management
- Browser automation
- Email support
- Calendar integration

### Version 0.4
- Vision (screen understanding)
- Wake word detection
- Local AI fallback

### Long-Term Vision

Build an AI operating system assistant comparable to the fictional Jarvis from Iron Man—capable of understanding context, assisting with everyday work, and interacting naturally with a computer.

---

## Installation

```bash
git clone https://github.com/adelekedavid2208-pixel/JavisAI

cd JarvisAI

pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Run:

```bash
python main.py
```

---

## Status

 Early Beta

The project is functional but under active development. Features, APIs, and architecture may change frequently.

---

## Contributing

Suggestions, issues, and pull requests are welcome.

---

## License

MIT License

---

## Author

David Adeleke

Building Jarvis in public.

Follow the journey on X:
https://x.com/adeleke8498
