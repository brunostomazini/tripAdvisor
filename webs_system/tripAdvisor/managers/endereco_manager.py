from .base_manager import BaseManager 

class EnderecoManager(BaseManager):
    
    def find_by_cep(self) -> list['Local']:
        return self.filter(cep__startswith='90')