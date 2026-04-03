"""
AtlasRad - URLs de l'application Authentification
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Inscription
    path('register/', views.register, name='register'),
    # Connexion (retourne JWT)
    path('login/', views.login, name='login'),
    # Renouvellement du token (avec refresh token)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Profil utilisateur connecté
    path('me/', views.my_profile, name='my_profile'),
]
