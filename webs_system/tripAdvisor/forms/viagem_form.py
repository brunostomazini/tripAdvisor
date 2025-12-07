from django import forms
from ..models import Viagem 
# Assumindo que Proposito e Transporte são importados através de .models
# Se Proposito e Transporte forem Enums em ..enum, você precisará importar:
# from ..enum import Proposito, Transporte 


class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        # Incluindo todos os campos da sua definição de modelo (exceto BaseModel, dono e m2m)
        fields = [
            'titulo', 'descricao', 'destino', 'pais_destino', 'inicio', 'final', 
            'orcamento', 'proposito', 'notas', 'transporte', 'atracoes'
        ]
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da viagem'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição detalhada'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade ou local de destino'}),
            'pais_destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País de destino'}),
            
            # CORREÇÃO CRÍTICA PARA DATAS: Usa type='date' para o seletor nativo do HTML5
            'inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'final': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            
            'orcamento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            
            # Usa form-select para campos de escolha
            'proposito': forms.Select(attrs={'class': 'form-select'}),
            'transporte': forms.Select(attrs={'class': 'form-select'}),
            
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas adicionais ou observações'}),

            # NOVO: Widget para o campo ManyToMany 'atracoes'. Permite selecionar múltiplas opções.
            'atracoes': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    # Sobrescreve o clean para forçar a execução da lógica de validação do modelo (final > inicio)
    def clean(self):
        cleaned_data = super().clean()
        try:
            # Garante que o método clean() definido no modelo Viagem seja executado.
            self.instance.clean()
        except forms.ValidationError as e:
            # Propaga as exceções de validação para o formulário
            self.add_error(None, e)
        return cleaned_data