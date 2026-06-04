BLOCKED_COMMANDS = [
    "delete system32",
    "format c",
    "rm -rf",
    "shutdown /s /f",
    "disable antivirus"
]


def is_safe(command: str):
    command = command.lower()

    for blocked in BLOCKED_COMMANDS:
        if blocked in command:
            return False

    return True