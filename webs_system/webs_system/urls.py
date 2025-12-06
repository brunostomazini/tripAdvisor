from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import *
from django.contrib.auth import views as auth_views
from .views import ProfileView
from .forms import CustomLoginForm


urlpatterns = [
    
    path('admin/', admin.site.urls),

    path('', Index.as_view(), name="index"),

    path('tripAdvisor/', include('tripAdvisor.urls', namespace='tripAdvisor')),
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name = "login.html", authentication_form = CustomLoginForm), name='login'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/profile/', ProfileView.as_view(), name='profile'),

    path('search/atracoes', LocalAndAtividadeListView.as_view(), name='search' )

]
