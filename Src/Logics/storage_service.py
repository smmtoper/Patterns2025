from Src.Models.storage_model import storage_model
from Src.Core.prototype import prototype
from Src.Core.observe_service import observe_service
from Src.Core.validator import validator, operation_exception
from Src.Dtos.storage_dto import storage_dto
from Src.Core.log_engine import log_engine


class storage_service:
    def __init__(self):
        self.storages = prototype([])
        observe_service.add(log_engine())

    def add(self, payload):
        if isinstance(payload, dict):
            dto = storage_dto().create(payload)
            model = storage_model.from_dto(dto, {})
        else:
            model = payload
            validator.validate(model, storage_model)
        for existing in self.storages.data:
            if existing.unique_code == model.unique_code:
                log_engine.error(f"Попытка добавить склад с уже существующим unique_code: {model.unique_code}")
                raise operation_exception("Item with same id already exists")
        self.storages.data.append(model)
        observe_service.create_event("add:storage", model)
        log_engine.info(f"Добавлен склад: {model.unique_code}")
        return model

    def update(self, unique_code, payload):
        target_index = None
        for i, existing in enumerate(self.storages.data):
            if existing.unique_code == unique_code:
                target_index = i
                break
        if target_index is None:
            log_engine.error(f"Склад с unique_code={unique_code} не найден для обновления")
            raise operation_exception("Item not found")
        if isinstance(payload, dict):
            dto = storage_dto().create(payload)
            model = storage_model.from_dto(dto, {})
            model.unique_code = unique_code
        else:
            model = payload
            validator.validate(model, storage_model)
            if model.unique_code != unique_code:
                model.unique_code = unique_code
        self.storages.data[target_index] = model
        observe_service.create_event("update:storage", model)
        log_engine.info(f"Обновлен склад: {model.unique_code}")
        return model

    def delete(self, unique_code):
        target = None
        for item in self.storages.data:
            if item.unique_code == unique_code:
                target = item
                break
        if target is None:
            log_engine.error(f"Склад с unique_code={unique_code} не найден для удаления")
            raise operation_exception("Item not found")
        observe_service.create_event("before_delete:storage", target)
        self.storages.data = [x for x in self.storages.data if x.unique_code != unique_code]
        observe_service.create_event("delete:storage", target)
        log_engine.info(f"Удален склад: {unique_code}")
        return True

    def get(self, unique_code):
        for item in self.storages.data:
            if item.unique_code == unique_code:
                log_engine.debug(f"Получен склад: {unique_code}")
                return item
        log_engine.debug(f"Склад с unique_code={unique_code} не найден")
        return None

    def get_all(self):
        log_engine.debug(f"Получены все склады, количество: {len(self.storages.data)}")
        return list(self.storages.data)
