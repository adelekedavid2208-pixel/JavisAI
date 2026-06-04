import webbrowser
import subprocess
from datetime import datetime
import urllib.parse
import shutil
import os


# ==============================
# APP LAUNCH SYSTEM
# ==============================

def open_app(name):
    name = (name or "").lower().strip()

    app_map = {
        "chrome": "chrome",
        "notepad": "notepad",
        "calculator": "calc",
        "calc": "calc",
        "file manager": "explorer",
        "file explorer": "explorer",
        "explorer": "explorer",
        "paint": "mspaint",
        "task manager": "taskmgr",
        "cmd": "cmd",
        "powershell": "powershell",
        "settings": "start ms-settings:",
        "store": "start ms-windows-store:",
        "microsoft store": "start ms-windows-store:",
        "control panel": "control",
        "remote desktop": "mstsc"
    }

    # exact match
    if name in app_map:
        cmd = app_map[name]

        try:
            if cmd.startswith("start "):
                subprocess.Popen(cmd, shell=True)
            else:
                subprocess.Popen(cmd)

            return f"Opening {name}."

        except Exception as e:
            return f"Failed to open {name}: {e}"

    # fallback: PATH
    if shutil.which(name):
        try:
            subprocess.Popen(name, shell=True)
            return f"Opening {name}."
        except Exception as e:
            return f"Failed to open {name}: {e}"

    # last fallback
    try:
        os.system(f"start {name}")
        return f"Trying to open {name}."
    except Exception as e:
        return f"I could not open {name}: {e}"


# ==============================
# WEB SEARCH
# ==============================

def web_search(query):
    url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)
    webbrowser.open(url)
    return f"Searching Google for {query}"


# ==============================
# TIME
# ==============================

def get_time():
    return datetime.now().strftime("%I:%M %p")


# ==============================
# DATE
# ==============================

def get_date():
    return datetime.now().strftime("%A, %d %B %Y")