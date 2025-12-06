from django import forms
from ..models import Avaliacao, Viagem # Importando Viagem também, caso Avaliacao a referencie

class AvaliacaoForm(forms.ModelForm):
    # O campo 'viagem' (ForeignKey) geralmente é excluído ou configurado
    # para não ser editável em um formulário de update de avaliação,
    # pois a avaliação já está vinculada a uma viagem.
    # Exemplo de configuração:
    viagem = forms.ModelChoiceField(
        queryset=Viagem.objects.all(),
        disabled=True, # Torna o campo não editável, apenas informativo
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Avaliacao
        # Campos que o usuário pode editar na avaliação
        fields = ('viagem', 'titulo', 'texto', 'nota')
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da sua avaliação'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Sua opinião detalhada...'}),
            'nota': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'placeholder': 'Nota (1 a 5)'}),
        }