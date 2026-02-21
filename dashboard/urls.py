from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
]