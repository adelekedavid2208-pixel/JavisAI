import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("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"))

def ask_jarvis(prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful AI assistant. Keep answers short and clear."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )

        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"Brain error: {e}"