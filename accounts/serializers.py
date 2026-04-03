"""
AtlasRad - Serializers des Utilisateurs
Valide et transforme les données d'entrée/sortie de l'API.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription d'un nouvel utilisateur."""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm',
                  'first_name', 'last_name', 'role', 'hospital', 'specialty']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'role': {'read_only': True},  # Le rôle ne peut pas être changé à l'inscription
        }

    def validate(self, attrs):
        """Vérification que les deux mots de passe correspondent."""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password": "Les deux mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        """Création de l'utilisateur avec mot de passe haché automatiquement."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)  # Hachage bcrypt automatique par Django
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer pour afficher et modifier le profil utilisateur."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'role', 'hospital', 'specialty', 'avatar', 'created_at']
        read_only_fields = ['id', 'username', 'role', 'created_at']


class LoginResponseSerializer(serializers.Serializer):
    """Serializer de réponse pour le login (documentation uniquement)."""
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserProfileSerializer()
