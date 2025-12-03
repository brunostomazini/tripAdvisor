from .base_form import BaseForm
from ..models.atracao import Atracao

class AtracaoForm(BaseForm):
    class Meta:
        model = Atracao
        fields = '__all__'
