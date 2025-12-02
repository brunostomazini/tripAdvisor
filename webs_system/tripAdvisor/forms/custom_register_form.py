from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from datetime import date
from ..models import Perfil 
from ..enum import Genero 


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email') + UserCreationForm.Meta.fields[2:] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class PerfilDataForm(forms.ModelForm):

    perfil_nome = forms.CharField(max_length=100, label="Nome Completo", validators=[MinLengthValidator(10)])

    class Meta:
        model = Perfil
        fields = (
            'email', 'perfil_nome', 'passaporte', 'data_nascimento', 'pais', 'genero', 
            'pagina_pessoal', 'biografia', 'lingua'
        )

    passaporte = forms.CharField(max_length=10, label="Passaporte", validators=[MinLengthValidator(10)])
    data_nascimento = forms.DateField(
        label="Data de Nascimento",
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'AAAA-MM-DD'}),
        error_messages={'invalid': 'Data deve ser no formato AAAA-MM-DD.'}
    )
    pais = forms.CharField(max_length=100, label="País", validators=[MinLengthValidator(3)])
    genero = forms.ChoiceField(choices=Genero.choices,label="Gênero",initial=Genero.NOT_INFORMED)
    biografia = forms.CharField(label="Biografia (Opcional)", widget=forms.Textarea(attrs={'rows': 3}), required=False)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento:
            today = date.today()
            age = today.year - data_nascimento.year - ((today.month, today.day) < (data_nascimento.month, data_nascimento.day))
            if age < 18:
                raise forms.ValidationError("Usuário precisa ter 18 anos ou mais!")
        return data_nascimento