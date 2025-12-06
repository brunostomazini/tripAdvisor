from django import forms
# Importe BaseForm se for uma classe que você define para estilização ou outros mixins
from .base_form import BaseForm 
from ..models.viagem import Viagem

class ViagemForm(BaseForm):
    class Meta:
        model = Viagem

        fields = '__all__'

        exclude = ('dono',)
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'pais_destino': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Tipos específicos como Date e Number Input
            'inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'final': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'orcamento': forms.NumberInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            # Campos de Escolha (Select)
            'proprosito': forms.Select(attrs={'class': 'form-select'}),
            'transporte': forms.Select(attrs={'class': 'form-select'}),
            
            # Campo Many-to-Many para Atrações
            'atracoes': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }