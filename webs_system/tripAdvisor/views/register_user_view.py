from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import transaction
from django.views import View 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from ..forms import UserRegistrationForm, PerfilDataForm 
from ..models import Perfil
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.http import Http404


class RegisterUserView(View):
    template_name = 'tripAdvisor/register.html'
    success_url = reverse_lazy('index')

    def get(self, request):
        user_form = UserRegistrationForm()
        perfi_form = PerfilDataForm()

        context = {
            'user_form': user_form,
            'perfi_form': perfi_form,
            'title': "Registro de Conta"
        }

        return render(request, self.template_name, context)

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        perfil_form = PerfilDataForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save() 

                    try:
                        comum_group = Group.objects.get(name='Comum')
                        user.groups.add(comum_group)
                    except Group.DoesNotExist:
                        print("WARNING: Django Grupo 'Comum' nao existe.")

                    perfil_data = perfil_form.cleaned_data
                    Perfil.objects.create(
                        user=user, 
                        email=user.email,
                        nome=perfil_data['perfil_nome'],
                        passaporte=perfil_data['passaporte'],
                        data_nascimento=perfil_data['data_nascimento'],
                        pais=perfil_data['pais'],
                        genero=perfil_data['genero'],
                        pagina_pessoal=perfil_data.get('pagina_pessoal'),
                        biografia=perfil_data.get('biografia'),
                        lingua=perfil_data.get('lingua'),
                    )
                    login(request, user)
                    return redirect(self.success_url) 
            except Exception as e:
                user_form.add_error(None, "Ocorreu um erro de sistema durante o cadastro. Tente novamente.")
                print(f"Registration transaction failed: {e}") 

        context = {
            'user_form': user_form,
            'perfil_form': perfil_form,
            'title': 'Registro de Conta'
        }
        return render(request, self.template_name, context)
    
class PerfilUpdateView(LoginRequiredMixin, UpdateView):

    model = Perfil
    form_class = PerfilDataForm 
    template_name = 'tripAdvisor/register.html' 
    success_url = reverse_lazy('profile') 

    def get_object(self, queryset=None):
        try:
            return self.request.user.perfil
        except Perfil.DoesNotExist:
            raise Http404("Perfil do usuário não encontrado. Por favor, crie seu perfil primeiro.")
