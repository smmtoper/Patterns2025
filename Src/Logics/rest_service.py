from Src.reposity import reposity
from Src.Models.settings_model import settings_model
from Src.settings_manager import settings_manager
from datetime import datetime
from Src.Core.prototype import prototype


# Сервис для расчета остатков
class rest_service:
    # Репозиторий
    __repo: reposity = reposity()

    # Текущие настройки
    __settings:settings_model = settings_manager().settings

    # Рассчитать остатки
    def calc(self) -> list:
        transactions = self.__repo.data[ reposity.transaction_key() ]
        for storage in self.__repo.data[  reposity.storage_key()  ]:
            items = prototype.clone(      )



