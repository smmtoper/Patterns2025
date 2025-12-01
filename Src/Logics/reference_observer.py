from Src.Core.observe_service import observe_service
from Src.Logics.rest_service import rest_service
from Src.Models.receipt_model import receipt_model
from Src.Models.rest_model import rest_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.storage_model import storage_model
from Src.Core.validator import validator, operation_exception

class reference_observer:
    def handle(self, event: str, params):
        if event == "delete":
            item = params
            if isinstance(item, nomenclature_model):
                rest_items = rest_service().calc()
                for rest in rest_items:
                    if rest.nomenclature.unique_code == item.unique_code:
                        raise operation_exception(f"Невозможно удалить номенклатуру {item.name}, она используется в остатках.")
            if isinstance(item, receipt_model):
                pass
        elif event == "update":
            item = params
            if isinstance(item, nomenclature_model):
                rest_items = rest_service().calc()
                for rest in rest_items:
                    if rest.nomenclature.unique_code == item.unique_code:
                        rest.nomenclature.name = item.name
