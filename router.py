from groq import Groq
import os
import json
import re

from memory import get_memory

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ==============================
# SAFE JSON EXTRACTION HELPERS
# ==============================

def _safe_json_load(content: str):
    """
    Extracts and parses JSON safely from LLM output.
    Handles cases like:
    - raw JSON
    - JSON inside text
    - malformed wrappers
    """

    if not content:
        return None

    content = content.strip()

    # Try direct parse first
    try:
        return json.loads(content)
    except:
        pass

    # Try extracting JSON block
    try:
        match = re.search(r"(\[.*\]|\{.*\})", content, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except:
        return None

    return None


def _normalize_plan(plan):
    """
    Ensures final output is ALWAYS:
    List[Dict]
    """

    if plan is None:
        return []

    # single dict → list
    if isinstance(plan, dict):
        plan = [plan]

    # string → try parse
    if isinstance(plan, str):
        parsed = _safe_json_load(plan)
        return _normalize_plan(parsed)

    normalized = []

    for step in plan:

        # stringified JSON inside list
        if isinstance(step, str):
            step = _safe_json_load(step)
            if not step:
                continue

        if isinstance(step, dict):
            normalized.append(step)

    return normalized


# ==============================
# MAIN ROUTER
# ==============================

def parse_intent(text: str):

    text = (text or "").strip()

    if not text:
        return [{"tool": "chat", "input": ""}]

    # ==========================
    # MEMORY CONTEXT
    # ==========================

    memory = get_memory(limit=10)
    memory_text = "\n".join([f"- {m['text']}" for m in memory])

    # ==========================
    # SYSTEM PROMPT
    # ==========================

    prompt = f"""
You are Jarvis Planner AI.

Convert user input into structured JSON actions.

========================
TOOLS AVAILABLE
========================

1. open_app
{{"tool":"open_app","name":"chrome"}}

2. web_search
{{"tool":"web_search","query":"AI news"}}

3. get_time
{{"tool":"get_time"}}

4. get_date
{{"tool":"get_date"}}

5. memory
{{"tool":"memory","action":"save","text":"..."}}  
{{"tool":"memory","action":"recall","query":"..."}}

6. chat
{{"tool":"chat","input":"..."}}

========================
CRITICAL RULES
========================

- Output MUST be valid JSON ONLY
- ALWAYS return a LIST of objects
- NEVER return strings inside the list
- NEVER add explanations
- NEVER use markdown
- If multiple actions exist, return multiple objects in list

Example correct output:
[
  {{"tool":"get_time"}},
  {{"tool":"web_search","query":"AI news"}}
]

========================
MEMORY
========================
{memory_text}

USER INPUT:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        raw_plan = _safe_json_load(content)

        plan = _normalize_plan(raw_plan)

        if not plan:
            return [{"tool": "chat", "input": text}]

        return plan

    except Exception as e:
        print("Router parse error:", e)

        return [{"tool": "chat", "input": text}]