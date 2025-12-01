from Src.Core.validator import validator
from Src.Dtos.filter_dto import filter_dto

class prototype:
    def __init__(self, data: list):
        validator.validate(data, list)
        self.__data = data

    @property
    def data(self):
        return self.__data

    def clone(self, data: list = None) -> "prototype":
        inner_data = data if data is not None else self.__data
        cloned_data = copy.deepcopy(inner_data)
        return prototype(cloned_data)

    @staticmethod
    def filter(data: list, filter_obj: filter_dto) -> list:
        if not data:
            return []

        validator.validate(filter_obj, filter_dto)
        result = []

        for item in data:
            if hasattr(item, filter_obj.field_name):
                value = getattr(item, filter_obj.field_name)
                if value == filter_obj.value:
                    result.append(item)

        return result
