from Src.Core.observe_service import observer, observe_service
from Src.settings_manager import settings_manager
import logging
import os

class log_observer(observer):
    def __init__(self):
        self.settings = settings_manager().settings
        log_cfg = getattr(self.settings, "logging", {})
        self.level_name = log_cfg.get("level", "DEBUG").upper()
        self.output = log_cfg.get("output", "console").lower()
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(getattr(logging, self.level_name, logging.DEBUG))
        self.logger.propagate = False

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

        if self.output == "file":
            os.makedirs("logs", exist_ok=True)
            file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def handle(self, event: str, params):
        msg = f"{event}: {params}"
        if self.level_name == "DEBUG":
            self.logger.debug(msg)
        elif self.level_name == "INFO":
            if event.lower() in ("add", "update", "delete", "web_call"):
                self.logger.info(msg)
        elif self.level_name == "ERROR":
            if "error" in event.lower():
                self.logger.error(msg)
