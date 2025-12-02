from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from webs_system.views import index
from django.contrib.auth import views as auth_views
from .views import ProfileView
from .forms import CustomLoginForm


urlpatterns = [
    
    path('admin/', admin.site.urls),

    path('', index, name="index"),

    path('tripadvisor/', include('tripAdvisor.urls')),
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name = "login.html", authentication_form = CustomLoginForm), name='login'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/profile/', ProfileView.as_view(), name='profile'),


]
