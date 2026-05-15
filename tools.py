import webbrowser
import subprocess
from datetime import datetime
import urllib.parse


def open_app(name):
    name = name.lower()

    if "chrome" in name:
        subprocess.Popen("start chrome", shell=True)
        return "Opening Chrome"

    if "notepad" in name:
        subprocess.Popen("notepad")
        return "Opening Notepad"

    if "calculator" in name:
        subprocess.Popen("calc")
        return "Opening Calculator"

    if "file" in name or "explorer" in name:
        subprocess.Popen("explorer")
        return "Opening File Explorer"

    return "App not found"


def web_search(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
    webbrowser.open(url)
    return f"Searching Google for {query}"


def get_time():
    return datetime.now().strftime("%I:%M %p")


def get_date():
    return datetime.now().strftime("%A, %d %B %Y")