import logging
from Src.Core.observe_service import observer


class file_log_observer(observer):
    """
    Наблюдатель, записывающий события в лог-файл.
    Использует встроенный модуль logging.
    """

    def __init__(self, file_name="log.txt", level=logging.INFO):
        self._file_name = file_name
        self._level = level
        self._logger = None

        self._init_logger()

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value
        self._init_logger()           # переинициализируем логгер

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        if self._logger:
            self._logger.setLevel(value)

    # -----------------------------
    #  Инициализация логгера
    # -----------------------------
    def _init_logger(self):
        """Создаёт logger и file handler. Защищено от ошибок."""
        try:
            self._logger = logging.getLogger(f"file_logger_{self._file_name}")

            handler = logging.FileHandler(self._file_name, encoding="utf-8")
            formatter = logging.Formatter('[%(levelname)s] %(message)s')
            handler.setFormatter(formatter)

            self._logger.handlers = []        # очищаем старые обработчики
            self._logger.addHandler(handler)
            self._logger.setLevel(self._level)

        except Exception as ex:
            logging.basicConfig(level=logging.ERROR)
            logging.error(f"Ошибка инициализации file_log_observer: {ex}")

    # -----------------------------
    #  Основной метод наблюдателя
    # -----------------------------
    def handle(self, event: str, params):
        """Принимает событие от лог-движка."""
        try:
            if self._logger:
                self._logger.info(f"[{event}] {params}")
        except Exception as ex:
            logging.error(f"Ошибка записи в лог-файл: {ex}")
