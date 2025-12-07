from Src.settings_manager import settings_manager

settings = settings_manager().settings

MIN_LEVEL = settings.min_log_level
LOG_TO_FILE = settings.log_to_file

LEVELS = {"DEBUG": 10, "INFO": 20, "ERROR": 30}

def log(level, message):
    if LEVELS[level] >= LEVELS[MIN_LEVEL]:
        line = f"[{level}] {message}"
        if LOG_TO_FILE:
            with open("app.log", "a", encoding="utf-8") as f:
                f.write(line + "\n")
        else:
            print(line)

def debug(msg): log("DEBUG", msg)
def info(msg): log("INFO", msg)
def error(msg): log("ERROR", msg)
