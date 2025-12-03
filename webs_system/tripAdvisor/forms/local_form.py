from django import forms
from .base_form import BaseForm
from ..models import Local
from django.forms import TimeInput, TextInput # Importando TimeInput e TextInput

class LocalForm(BaseForm):
    class Meta:
        model = Local
        fields = '__all__'
        exclude = ['endereco'] 

        widgets = {
            # Aplicando TimeInput e classe Bootstrap para campos de hora
            'hora_abertura': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fechamento': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            
            # Aplicando classe Bootstrap para outros campos (se BaseForm não fizer isso)
            'nome': TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nota': TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            # O campo 'ingresso' é um CheckboxInput e geralmente precisa apenas da classe 'form-check-input', 
            # que é tratada pelo loop especial no template.
        }