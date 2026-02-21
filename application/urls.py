from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirection page d'accueil
    path('', RedirectView.as_view(url='/etudiants/liste/')),

    # Applications principales
    path('etudiants/', include('etudiants.urls')),
    path('cours/', include('cours.urls')),
    path('evaluation/', include('evaluation.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('stats/', include('statistique.urls')),
]