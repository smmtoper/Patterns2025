from Src.Models.settings_model import settings_model
from Src.Models.company_model import company_model
from Src.Core.validator import validator, operation_exception
from Src.Core.common import common
from Src.Core.response_formats import response_formats
from Src.Core.abstract_manager import abstract_manager
from Src.Core.observe_service import observe_service
from Src.Core.log_engine import LogEngine

import json, os
from datetime import datetime

class settings_manager(abstract_manager):
    __settings: settings_model = None
    DATE_FORMAT = "%Y-%m-%d"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__set_default()
        observe_service.add(self)

    @property
    def settings(self) -> settings_model:
        return self.__settings

    @property
    def min_log_level(self):
        return self.__settings.min_log_level

    @min_log_level.setter
    def min_log_level(self, value: str):
        if value not in ("DEBUG", "INFO", "ERROR"):
            raise ValueError("Недопустимый уровень логирования")
        old = self.__settings.min_log_level
        self.__settings.min_log_level = value
        LogEngine.set_level(value)
        observe_service.create_event("settings_changed", {"field": "min_log_level", "old": old, "new": value})

    @property
    def log_to_file(self):
        return self.__settings.log_to_file

    @log_to_file.setter
    def log_to_file(self, value: bool):
        old = self.__settings.log_to_file
        self.__settings.log_to_file = bool(value)
        LogEngine.set_output(to_file=bool(value))
        observe_service.create_event("settings_changed", {"field": "log_to_file", "old": old, "new": value})

    def load(self) -> bool:
        if not self.file_name:
            raise operation_exception("Не найден файл настроек!")

        if not os.path.exists(self.file_name):
            LogEngine.error(f"Файл настроек '{self.file_name}' не найден")
            return False

        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)

            LogEngine.info(f"Настройки загружены из {self.file_name}")

            self.__apply_company(data)
            self.__apply_default_format(data)
            self.__apply_block_period(data)
            self.__apply_log_settings(data)

            return True

        except Exception as e:
            LogEngine.error(f"Ошибка загрузки настроек: {e}")
            return False

    def __apply_company(self, data: dict):
        company_block = data.get("company", {})
        validator.validate(company_block, dict)
        fields = common.get_fields(self.__settings.company)
        for key, value in company_block.items():
            if key in fields:
                setattr(self.__settings.company, key, value)

    def __apply_default_format(self, data: dict):
        fmt = data.get("default_format", "markdown")
        if fmt not in response_formats.list_all_formats():
            fmt = "markdown"
        self.__settings.default_response_format = fmt

    def __apply_block_period(self, data: dict):
        raw = data.get("block_period", None)
        if raw is None:
            self.__settings.block_period = None
            return
        try:
            if isinstance(raw, str):
                dt = datetime.strptime(raw, self.DATE_FORMAT)
            elif isinstance(raw, datetime):
                dt = raw
            else:
                raise ValueError("block_period должен быть датой или строкой")
            self.__settings.block_period = dt
        except Exception:
            self.__settings.block_period = None

    def __apply_log_settings(self, data: dict):
        level = data.get("min_log_level", "INFO")
        if level not in ("DEBUG", "INFO", "ERROR"):
            level = "INFO"
        self.__settings.min_log_level = level
        LogEngine.set_level(level)

        to_file = bool(data.get("log_to_file", False))
        self.__settings.log_to_file = to_file
        LogEngine.set_output(to_file=to_file)

    def __set_default(self):
        company = company_model()
        company.name = "Рога и копыта"
        company.inn = -1
        self.__settings = settings_model()
        self.__settings.company = company
        self.__settings.default_response_format = "markdown"
        self.__settings.block_period = None
        self.__settings.min_log_level = "INFO"
        self.__settings.log_to_file = False

    def save(self):
        try:
            data = {
                "company": {"name": self.settings.company.name, "inn": self.settings.company.inn},
                "default_format": self.settings.default_response_format,
                "block_period": self.settings.block_period.strftime(self.DATE_FORMAT) if self.settings.block_period else None,
                "min_log_level": self.settings.min_log_level,
                "log_to_file": self.settings.log_to_file
            }
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            LogEngine.info(f"Настройки сохранены в {self.file_name}")
            observe_service.create_event("settings_saved", data)
        except Exception as e:
            LogEngine.error(f"Ошибка сохранения настроек: {e}")
