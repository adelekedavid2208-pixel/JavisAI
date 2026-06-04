import queue
import threading

# =========================
# REAL-TIME SYSTEM QUEUES
# =========================

# incoming user commands
text_queue = queue.Queue()

# outgoing Jarvis speech
speech_queue = queue.Queue()

# =========================
# SPEECH STATE LOCK
# =========================

# True while Jarvis is speaking
is_speaking = threading.Event()