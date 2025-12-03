from .base_form import BaseForm
from ..models import Atividade

class AtividadeForm(BaseForm):
    class Meta:
        model = Atividade
        fields = '__all__'

