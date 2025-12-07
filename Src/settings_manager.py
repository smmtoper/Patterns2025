from Src.Models.settings_model import settings_model
from Src.Models.company_model import company_model
from Src.Core.validator import validator, operation_exception
from Src.Core.common import common
from Src.Core.response_formats import response_formats
from Src.Core.abstract_manager import abstract_manager
import json, os
from datetime import datetime
from Src.Core.log_engine import log_engine

class settings_manager(abstract_manager):

    __settings: settings_model = None
    DATE_FORMAT = "%Y-%m-%d"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__set_default()

    @property
    def settings(self) -> settings_model:
        return self.__settings

    def load(self) -> bool:
        if not self.file_name:
            raise operation_exception("Не найден файл настроек!")

        if not os.path.exists(self.file_name):
            log_engine.error(f"Файл настроек '{self.file_name}' не найден")
            return False

        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)

            log_engine.info(f"Настройки загружены из {self.file_name}")

            self.__apply_company(data)
            self.__apply_default_format(data)
            self.__apply_block_period(data)
            self.__apply_log_settings(data)

            return True

        except Exception as e:
            log_engine.error(f"Ошибка загрузки настроек: {e}")
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

        self.__settings.log_to_file = bool(data.get("log_to_file", False))

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
