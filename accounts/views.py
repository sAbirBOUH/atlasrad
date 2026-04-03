"""
AtlasRad - Views Authentification
POST /api/auth/register  -> Inscription
POST /api/auth/login     -> Connexion (JWT)
GET  /api/auth/me        -> Profil utilisateur connecté
PATCH /api/auth/me       -> Modifier le profil
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User
from .serializers import RegisterSerializer, UserProfileSerializer


def get_tokens_for_user(user):
    """Génère une paire de tokens JWT (access + refresh) pour un utilisateur."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Inscription d'un nouveau radiologue / technicien.
    Body: { username, email, password, password_confirm, first_name, last_name, hospital, specialty }
    """
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)

        return Response({
            "error": False,
            "message": f"Bienvenue sur AtlasRad, Dr {user.first_name or user.username} !",
            "tokens": tokens,
            "user": UserProfileSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    return Response({
        "error": True,
        "message": "Erreur de validation. Corrigez les champs indiqués.",
        "details": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Connexion d'un utilisateur existant.
    Body: { username, password }
    Retourne: { access, refresh, user }
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            "error": True,
            "message": "Identifiant et mot de passe requis."
        }, status=status.HTTP_400_BAD_REQUEST)

    # Django authentifie et vérifie le hash du mot de passe
    user = authenticate(username=username, password=password)

    if user is None:
        return Response({
            "error": True,
            "message": "Identifiants incorrects. Vérifiez votre nom d'utilisateur et mot de passe."
        }, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({
            "error": True,
            "message": "Ce compte est désactivé. Contactez l'administrateur."
        }, status=status.HTTP_403_FORBIDDEN)

    tokens = get_tokens_for_user(user)

    return Response({
        "error": False,
        "message": f"Connexion réussie. Bienvenue {user.first_name or user.username} !",
        "tokens": tokens,
        "user": UserProfileSerializer(user).data
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    """
    GET  -> Retourne le profil de l'utilisateur connecté
    PATCH -> Met à jour les informations du profil
    """
    user = request.user

    if request.method == 'GET':
        return Response({
            "error": False,
            "user": UserProfileSerializer(user).data
        })

    elif request.method == 'PATCH':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "error": False,
                "message": "Profil mis à jour avec succès.",
                "user": serializer.data
            })
        return Response({
            "error": True,
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
