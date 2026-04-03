"""
AtlasRad - URLs de l'application Analyses
"""
from django.urls import path
from . import views

urlpatterns = [
    # Upload d'une image médicale (multipart/form-data)
    path('upload/', views.upload_image, name='upload-image'),

    # Déclenchement de l'analyse IA
    path('analyze/', views.analyze_image, name='analyze-image'),

    # Historique des analyses de l'utilisateur
    path('history/', views.history, name='history'),

    # Stats du dashboard (admin uniquement)
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
]
