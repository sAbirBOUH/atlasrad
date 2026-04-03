"""
AtlasRad - URLs racine (routeur principal)
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Interface Admin Django
    path('admin/', admin.site.urls),

    # API : Authentification
    path('api/auth/', include('accounts.urls')),

    # API : Analyses (upload, analyze, history)
    path('api/analyses/', include('analyses.urls')),
]

# Servir les fichiers media (images uploadées) en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
