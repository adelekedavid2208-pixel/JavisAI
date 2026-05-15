from groq import Groq
import os
import json
from memory import get_context

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def parse_intent(text):
    context = get_context()

    prompt = f"""
You are Jarvis, an AI assistant with memory and planning ability.

You must output ONLY valid JSON.

TOOLS:
1. open_app -> {{"tool":"open_app","name":"chrome"}}
2. web_search -> {{"tool":"web_search","query":"..."}}
3. get_time -> {{"tool":"get_time"}}
4. get_date -> {{"tool":"get_date"}}
5. chat -> {{"tool":"chat","input":"..."}}

RULES:
- ALWAYS return JSON only
- ALWAYS include "tool"
- Use memory context below if relevant
- Break complex tasks into single best action

MEMORY:
{context}

USER:
{text}
"""

    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return json.loads(res.choices[0].message.content)

    except:
        return {"tool": "chat", "input": text}