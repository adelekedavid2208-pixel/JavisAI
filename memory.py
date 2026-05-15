import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"chat": []}

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def add_memory(role, content):
    memory = load_memory()

    memory["chat"].append({
        "role": role,
        "content": content
    })

    # keep last 20 messages only (prevents bloat)
    memory["chat"] = memory["chat"][-20:]

    save_memory(memory)


def get_context():
    memory = load_memory()
    return memory["chat"]