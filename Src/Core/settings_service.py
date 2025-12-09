import json
from Src.Core.observe_service import create_event


class settings_service:
    CONFIG_PATH = "settings.json"

    @staticmethod
    def load():
        """Загружает настройки из файла и отправляет событие наблюдателям."""
        try:
            with open(settings_service.CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        except Exception as e:
            create_event("error", f"Ошибка чтения файла настроек: {e}")
            return {}

        # уведомляем наблюдателей, что настройки загружены
        create_event("settings_loaded", data)
        return data

    @staticmethod
    def save(settings: dict):
        """Сохраняет настройки в файл и уведомляет наблюдателей."""
        try:
            with open(settings_service.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            create_event("error", f"Ошибка записи файла настроек: {e}")
            return

        create_event("settings_saved", settings)

    @staticmethod
    def update(key, value):
        """Обновляет одну настройку и уведомляет наблюдателей."""
        settings = settings_service.load()
        settings[key] = value
        settings_service.save(settings)

        create_event("settings_updated", {key: value})
