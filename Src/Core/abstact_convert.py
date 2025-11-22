
import abc
from Src.Core.validator import validator, argument_exception
from Src.Core.abstract_logic import abstract_logic

# Абстрактный класс для инкапсулирования логики связанной с сериализацией и десериализацией данных в словарь
class abstract_convert(abstract_logic):
    __error_text:str = ""

    """
    Сконвертировать объект в словарь
    """
    @abc.abstractmethod
    def serialize(self, field: str, object) -> dict:
        validator.validate(field, str)

    """
    Сконвертировать словарь в объект
    """
    @abc.abstractmethod
    def deserialize(self, data , field: str, instance):
        validator.validate(field, str)
        if data is None:
            return None
        elif instance is None:
            raise argument_exception("Не указан тип данных для конвертации!")

    
       
