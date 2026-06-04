import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"
MAX_FACTS = 200   # prevents memory from growing endlessly


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"facts": []}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"facts": []}


def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_memory(text):
    text = text.strip()
    if not text:
        return

    data = load_memory()

    # prevent duplicates
    existing = [fact["text"].lower() for fact in data["facts"]]
    if text.lower() in existing:
        return

    data["facts"].append({
        "text": text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # limit memory size
    if len(data["facts"]) > MAX_FACTS:
        data["facts"] = data["facts"][-MAX_FACTS:]

    save_memory(data)


def get_memory(limit=10):
    data = load_memory()
    return data["facts"][-limit:]


def clear_memory():
    save_memory({"facts": []})