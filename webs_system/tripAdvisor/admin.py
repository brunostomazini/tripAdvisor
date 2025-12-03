from django.contrib import admin
from .models import Perfil, Viagem, Endereco, Categoria, Local, Questao, Resposta, Avaliacao


# Register your models here.
admin.site.register(Perfil)
admin.site.register(Viagem)
admin.site.register(Endereco)
admin.site.register(Categoria)
admin.site.register(Local)

admin.site.register(Questao)
admin.site.register(Resposta)
admin.site.register(Avaliacao)
