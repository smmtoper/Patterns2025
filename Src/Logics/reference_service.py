from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.storage_model import storage_model
from Src.Core.prototype import prototype
from Src.Core.observe_service import observe_service
from Src.Core.validator import validator
from Src.Logics.reference_observer import reference_observer

class reference_service:
    def __init__(self):
        self.nomenclatures = prototype([])
        self.ranges = prototype([])
        self.categories = prototype([])
        self.storages = prototype([])
        observe_service.add(reference_observer())

    def add_nomenclature(self, item: nomenclature_model):
        validator.validate(item, nomenclature_model)
        self.nomenclatures.data.append(item)

    def update_nomenclature(self, item: nomenclature_model):
        validator.validate(item, nomenclature_model)
        for idx, existing in enumerate(self.nomenclatures.data):
            if existing.unique_code == item.unique_code:
                self.nomenclatures.data[idx] = item
                observe_service.create_event("update", item)
                break

    def delete_nomenclature(self, item: nomenclature_model):
        validator.validate(item, nomenclature_model)
        self.nomenclatures.data = [x for x in self.nomenclatures.data if x.unique_code != item.unique_code]
        observe_service.create_event("delete", item)

    def get_nomenclature(self, unique_code: str):
        for item in self.nomenclatures.data:
            if item.unique_code == unique_code:
                return item
        return None

    def add_range(self, item: range_model):
        validator.validate(item, range_model)
        self.ranges.data.append(item)

    def update_range(self, item: range_model):
        validator.validate(item, range_model)
        for idx, existing in enumerate(self.ranges.data):
            if existing.unique_code == item.unique_code:
                self.ranges.data[idx] = item
                observe_service.create_event("update", item)
                break

    def delete_range(self, item: range_model):
        validator.validate(item, range_model)
        self.ranges.data = [x for x in self.ranges.data if x.unique_code != item.unique_code]
        observe_service.create_event("delete", item)

    def get_range(self, unique_code: str):
        for item in self.ranges.data:
            if item.unique_code == unique_code:
                return item
        return None

    def add_category(self, item: category_model):
        validator.validate(item, category_model)
        self.categories.data.append(item)

    def update_category(self, item: category_model):
        validator.validate(item, category_model)
        for idx, existing in enumerate(self.categories.data):
            if existing.unique_code == item.unique_code:
                self.categories.data[idx] = item
                observe_service.create_event("update", item)
                break

    def delete_category(self, item: category_model):
        validator.validate(item, category_model)
        self.categories.data = [x for x in self.categories.data if x.unique_code != item.unique_code]
        observe_service.create_event("delete", item)

    def get_category(self, unique_code: str):
        for item in self.categories.data:
            if item.unique_code == unique_code:
                return item
        return None

    def add_storage(self, item: storage_model):
        validator.validate(item, storage_model)
        self.storages.data.append(item)

    def update_storage(self, item: storage_model):
        validator.validate(item, storage_model)
        for idx, existing in enumerate(self.storages.data):
            if existing.unique_code == item.unique_code:
                self.storages.data[idx] = item
                observe_service.create_event("update", item)
                break

    def delete_storage(self, item: storage_model):
        validator.validate(item, storage_model)
        self.storages.data = [x for x in self.storages.data if x.unique_code != item.unique_code]
        observe_service.create_event("delete", item)

    def get_storage(self, unique_code: str):
        for item in self.storages.data:
            if item.unique_code == unique_code:
                return item
        return None
