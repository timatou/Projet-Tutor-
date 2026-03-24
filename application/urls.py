from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirection page d'accueil
    path('', RedirectView.as_view(url='/dashboard')),

    # Authentification
    path('login/', auth_views.LoginView.as_view(template_name='utilisateurs/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Applications principales
    path('etudiants/', include('etudiants.urls')),
    path('utilisateurs/', include('utilisateurs.urls')),
    path('cours/', include('cours.urls')),
    path('evaluation/', include('evaluation.urls')),
    path('statistique/', include('statistique.urls')),
    path('dashboard/', include('dashboard.urls')),
]