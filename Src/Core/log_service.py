from Src.Core.log_level import log_level
from Src.Core.log_event import log_event
from Src.Core.settings_service import settings_service

class log_service:
    observers = []
    min_level = log_level.DEBUG

    @staticmethod
    def load_settings():
        cfg = settings_service.load()
        lvl = cfg.get("min_log_level", "DEBUG")
        log_service.min_level = log_level[lvl]

    @staticmethod
    def add(observer):
        log_service.observers.append(observer)

    @staticmethod
    def write(category, message):
        if category.value < log_service.min_level.value:
            return
        event = log_event(category.name, message)
        for obs in log_service.observers:
            obs.handle(event)
