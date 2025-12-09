from Src.Core.observe_service import observer
import logging

class console_log_observer(observer):
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger("console_logger")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(level)

    def handle(self, event: str, params):
        self.logger.info(f"[{event}] {params}")
