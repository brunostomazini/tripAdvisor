from django import forms
from ..models import Avaliacao

class AvaliacaoForm(forms.ModelForm):

    class Meta:
        model = Avaliacao
        fields = ('titulo', 'texto', 'nota', 'data_visita')

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da sua avaliação'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Sua opinião detalhada...'}),
            'nota': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10, 'placeholder': 'Nota (0 a 10)'}),
            'data_visita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }