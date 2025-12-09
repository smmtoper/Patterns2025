import os
from datetime import datetime
from Src.Core.observe_service import observe_service
from Src.Core.log_level import log_level


class LogEngine:
    """
    Центральный механизм логирования.
    """

    _instance = None

    @staticmethod
    def instance():
        """Singleton access"""
        if LogEngine._instance is None:
            LogEngine._instance = LogEngine()
        return LogEngine._instance

    def __init__(self):
        self.min_level = log_level.INFO      # по умолчанию
        self.log_file_path = "system.log"   # только если нужно
        self._initialized = True

    def set_min_level(self, level: int):
        """Устанавливает минимальный уровень логирования"""
        self.min_level = level

    def set_file(self, file_path: str):
        """Изменяет целевой файл логирования"""
        self.log_file_path = file_path

    def log(self, level: int, event: str, params):
        """
        Основной метод логирования.
        """

        if level < self.min_level:
            return  # фильтрация по уровню

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = {
            "timestamp": timestamp,
            "level": log_level.to_text(level),
            "event": event,
            "params": params
        }

        try:
            observe_service.create_event("log", message)
        except Exception as ex:
            self._write_fallback(ex, message)

    def _write_fallback(self, error, message):

        try:
            with open("fatal_log_engine.log", "a", encoding="utf-8") as f:
                f.write(f"[FATAL] Logging failed: {error}\nMsg: {message}\n")
        except:
            pass   # совсем аварийная ситуация
