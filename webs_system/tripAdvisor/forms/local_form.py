from .base_form import BaseForm
from ..models import Local

class LocalForm(BaseForm):
    class Meta:
        model = Local
        fields = '__all__'