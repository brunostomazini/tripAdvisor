from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

class ProfileView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        context = {
            'usuario':request.user,
        }
        return render(request, 'profile.html', context)