import os
from groq import Groq
from dotenv import load_dotenv

from memory import get_memory, add_memory

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================================
# MAIN AI BRAIN
# =========================================

def ask_jarvis(prompt: str) -> str:

    prompt = prompt.strip()

    if not prompt:
        return "I didn't catch that."

    lower_prompt = prompt.lower()

    # =====================================
    # DIRECT MEMORY SAVE
    # =====================================

    if lower_prompt.startswith("remember "):

        fact = prompt[9:].strip()

        if fact:

            add_memory(fact)

            return f"Okay. I will remember that {fact}."

        return "I did not receive anything to remember."

    if lower_prompt.startswith("save this "):

        fact = prompt[10:].strip()

        if fact:

            add_memory(fact)

            return "Saved."

        return "Nothing was provided to save."

    # =====================================
    # LOAD MEMORY
    # =====================================

    memory_facts = get_memory(limit=15)

    memory_lines = []

    for item in memory_facts:

        text = item.get("text", "").strip()

        if text:

            memory_lines.append(
                f"USER FACT: {text}"
            )

    memory_text = "\n".join(memory_lines)

    # =====================================
    # SYSTEM PROMPT
    # =====================================

    system_prompt = f"""
You are Jarvis, an advanced AI assistant running on a Windows PC.

You are speaking TO the user.

The memory facts below belong to the USER, not you.

IMPORTANT RULES:

- Never confuse the user's identity with your own
- If the user asks:
  - what is my name
  - what is my favorite color
  - where do I live
  use MEMORY facts to answer

- Keep answers concise and natural
- Do not roleplay
- Do not invent fake memory
- If memory exists, prioritize it

USER MEMORY:
{memory_text}
"""

    # =====================================
    # AI RESPONSE
    # =====================================

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=200
        )

        answer = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        # =================================
        # AUTO SAVE BASIC PERSONAL FACTS
        # =================================

        auto_memory_triggers = [
            "my name is",
            "i live in",
            "my favorite",
            "i am"
        ]

        if any(
            trigger in lower_prompt
            for trigger in auto_memory_triggers
        ):

            add_memory(prompt)

        return answer

    except Exception as e:

        return f"Brain error: {e}"