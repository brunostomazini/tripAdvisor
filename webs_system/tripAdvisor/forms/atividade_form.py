from django import forms
from django.forms import TimeInput, TextInput
from .base_form import BaseForm
from ..models import Atividade

class AtividadeForm(BaseForm):
    class Meta:
        model = Atividade
        fields = '__all__'

    widgets = {
            'nome': TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nota': TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'duracao_horas': TextInput(attrs={'class': 'form-control'}),
        }
