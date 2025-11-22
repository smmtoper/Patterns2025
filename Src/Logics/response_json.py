from Src.Core.abstract_response import abstract_response

# Преобразовать список в Json
class response_json(abstract_response):
    
    # Сформировать 
    def build(self, data: list) -> str:
        text = super().build( data )
        return ""
