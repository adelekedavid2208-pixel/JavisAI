import webbrowser
import subprocess
from datetime import datetime


def run_command(command: str):
    command = command.lower()

    # OPEN APPS
    if "open chrome" in command:
        subprocess.Popen("start chrome", shell=True)
        return "Opening Chrome."

    if "open notepad" in command:
        subprocess.Popen("notepad")
        return "Opening Notepad."

    if "open calculator" in command or "open calc" in command:
        subprocess.Popen("calc")
        return "Opening Calculator."

    if "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com/")
        return "Opening WhatsApp Web."

    # GOOGLE SEARCH (ROBUST VERSION)
    if "search" in command and "google" in command:
        query = command

        for word in ["search", "google", "for", "on"]:
            query = query.replace(word, "")

        query = query.strip()

        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            return f"Searching Google for {query}."

    # TIME
    if "time" in command:
        now = datetime.now().strftime("%I:%M %p")
        return f"The time is {now}."

    # DATE
    if "date" in command:
        today = datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {today}."

    return None