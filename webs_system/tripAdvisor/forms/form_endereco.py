from django import forms
from django.forms import TimeInput, TextInput
from .base_form import BaseForm
from ..models import  Endereco

class EnderecoForm(BaseForm):
    class Meta:
        model = Endereco
        fields = '__all__'
class Meta:
        model = Endereco
        fields = '__all__'
        labels = {
            'cep': 'CEP (apenas 8 dígitos)',
            'logradouro': 'Logradouro (Rua, Avenida, etc.)',
            'numero': 'Número',
            'complemento': 'Complemento (Ex: Apto 101, Bloco A)',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'estado': 'Estado/Província',
            'pais': 'País',
        }
        widgets = {
            'cep': TextInput(attrs={'class': 'form-control'}),
            'logradouro': TextInput(attrs={'class': 'form-control'}),
            'numero': TextInput(attrs={'class': 'form-control'}),
            'complemento': TextInput(attrs={'class': 'form-control'}),
            'bairro': TextInput(attrs={'class': 'form-control'}),
            'cidade': TextInput(attrs={'class': 'form-control'}),
            'estado': TextInput(attrs={'class': 'form-control'}),
            'pais': TextInput(attrs={'class': 'form-control'}),
        }