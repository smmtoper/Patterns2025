from Src.Core.validator import operation_exception
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model as category_model
from Src.Models.storage_model import storage_model
from Src.Models.receipt_model import receipt_model
from Src.Models.rest_model import rest_model
from Src.Logics.rest_service import rest_service


class reference_observer:


    def _get_all_rests(self):
        return rest_service().calc()

    def _raise_used_error(self, item, where: str, detail: str):
        raise operation_exception(
            f"Невозможно удалить {item.__class__.__name__} '{item.name}'. "
            f"Она используется в {where}: {detail}"
        )


    def _handle_delete_nomenclature(self, item: nomenclature_model):
        rests = self._get_all_rests()
        for rest in rests:
            if rest.nomenclature.unique_code == item.unique_code:
                self._raise_used_error(item, "остатках", rest.storage.name)

    def _handle_delete_range(self, item: range_model):
        rests = self._get_all_rests()
        for rest in rests:
            if rest.range.unique_code == item.unique_code:
                self._raise_used_error(item, "остатках", rest.storage.name)

    def _handle_delete_category(self, item: category_model):
        rests = self._get_all_rests()
        for rest in rests:
            if rest.category.unique_code == item.unique_code:
                self._raise_used_error(item, "остатках", rest.storage.name)

    def _handle_delete_storage(self, item: storage_model):
        rests = self._get_all_rests()
        for rest in rests:
            if rest.storage.unique_code == item.unique_code:
                self._raise_used_error(item, "остатках", "остатках")


    def _handle_update_nomenclature(self, item: nomenclature_model):
        rests = self._get_all_rests()
        for rest in rests:
            if rest.nomenclature.unique_code == item.unique_code:
                rest.nomenclature.name = item.name
                rest.nomenclature.category = item.category
                rest.nomenclature.range = item.range

    def _handle_update_range(self, item: range_model):
        rests = self._get_all_rests()
        for rest in rests:
            if rest.range.unique_code == item.unique_code:
                rest.range.name = item.name
                rest.range.short_name = item.short_name

    def _handle_update_category(self, item: category_model):
        rests = self._get_all_rests()
        for rest in rests:
            if rest.category.unique_code == item.unique_code:
                rest.category.name = item.name

    def _handle_update_storage(self, item: storage_model):
        rests = self._get_all_rests()
        for rest in rests:
            if rest.storage.unique_code == item.unique_code:
                rest.storage.name = item.name


    def handle(self, event: str, params):
        item = params

        if event == "delete":
            if isinstance(item, nomenclature_model):
                self._handle_delete_nomenclature(item)
            elif isinstance(item, range_model):
                self._handle_delete_range(item)
            elif isinstance(item, category_model):
                self._handle_delete_category(item)
            elif isinstance(item, storage_model):
                self._handle_delete_storage(item)

        elif event == "update":
            if isinstance(item, nomenclature_model):
                self._handle_update_nomenclature(item)
            elif isinstance(item, range_model):
                self._handle_update_range(item)
            elif isinstance(item, category_model):
                self._handle_update_category(item)
            elif isinstance(item, storage_model):
                self._handle_update_storage(item)
