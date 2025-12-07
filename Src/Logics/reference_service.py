from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model as category_model
from Src.Models.storage_model import storage_model
from Src.Core.prototype import prototype
from Src.Core.observe_service import observe_service
from Src.Core.validator import validator, operation_exception
from Src.Logics.reference_observer import reference_observer
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.storage_dto import storage_dto

class reference_service:
    def __init__(self):
        self.nomenclatures = prototype([])
        self.ranges = prototype([])
        self.categories = prototype([])
        self.storages = prototype([])
        observe_service.add(reference_observer())

    def _type_map(self, reference_type: str):
        t = reference_type.lower()
        if t in ("nomenclature", "nomenclatures"):
            return "nomenclature", self.nomenclatures, nomenclature_dto, nomenclature_model
        if t in ("range", "ranges", "unit", "units"):
            return "range", self.ranges, range_dto, range_model
        if t in ("category", "categories", "group", "groups"):
            return "category", self.categories, category_dto, category_model
        if t in ("storage", "storages", "warehouse"):
            return "storage", self.storages, storage_dto, storage_model
        raise operation_exception("Unsupported reference type")

    def add(self, reference_type: str, payload):
        _, collection, dto_cls, model_cls = self._type_map(reference_type)
        if isinstance(payload, dict):
            dto = dto_cls().create(payload)
            model = model_cls.from_dto(dto, {}) if hasattr(model_cls, "from_dto") else None
            if model is None:
                raise operation_exception("Cannot convert dto to model")
        else:
            model = payload
            validator.validate(model, model_cls)
        for existing in collection.data:
            if getattr(existing, "unique_code", None) == getattr(model, "unique_code", None):
                raise operation_exception("Item with same id already exists")
        collection.data.append(model)
        observe_service.create_event("add", model)
        observe_service.create_event("log_debug", f"Added {reference_type}: {model}")
        return model

    def update(self, reference_type: str, unique_code: str, payload):
        _, collection, dto_cls, model_cls = self._type_map(reference_type)
        target_index = None
        for i, existing in enumerate(collection.data):
            if getattr(existing, "unique_code", None) == unique_code:
                target_index = i
                break
        if target_index is None:
            raise operation_exception("Item not found")
        if isinstance(payload, dict):
            dto = dto_cls().create(payload)
            model = model_cls.from_dto(dto, {}) if hasattr(model_cls, "from_dto") else None
            if model is None:
                raise operation_exception("Cannot convert dto to model")
            model.unique_code = unique_code
        else:
            model = payload
            validator.validate(model, model_cls)
            if getattr(model, "unique_code", None) != unique_code:
                model.unique_code = unique_code
        collection.data[target_index] = model
        observe_service.create_event("update", model)
        observe_service.create_event("log_debug", f"Updated {reference_type}: {model}")
        return model

    def delete(self, reference_type: str, unique_code: str):
        _, collection, _, _ = self._type_map(reference_type)
        target = None
        for item in collection.data:
            if getattr(item, "unique_code", None) == unique_code:
                target = item
                break
        if target is None:
            raise operation_exception("Item not found")
        observe_service.create_event("before_delete", target)
        collection.data = [x for x in collection.data if getattr(x, "unique_code", None) != unique_code]
        observe_service.create_event("delete", target)
        observe_service.create_event("log_debug", f"Deleted {reference_type}: {target}")
        return True
