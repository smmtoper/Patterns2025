from Src.Core.observe_service import observer
import logging

class file_log_observer(observer):
    def __init__(self, file_name="log.txt", level=logging.INFO):
        self.logger = logging.getLogger("file_logger")
        handler = logging.FileHandler(file_name, encoding="utf-8")
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(level)

    def handle(self, event: str, params):
        self.logger.info(f"[{event}] {params}")
