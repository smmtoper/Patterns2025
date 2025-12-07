import json


class settings_service:
    CONFIG_PATH = "settings.json"
    cache = None

    @staticmethod
    def load():
        if settings_service.cache is None:
            with open(settings_service.CONFIG_PATH, "r", encoding="utf-8") as f:
                settings_service.cache = json.load(f)
        return settings_service.cache

    @staticmethod
    def get(key, default=None):
        config = settings_service.load()
        return config.get(key, default)

    @staticmethod
    def set(key, value):
        config = settings_service.load()
        config[key] = value
        with open(settings_service.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
