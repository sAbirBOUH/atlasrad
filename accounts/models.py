"""
AtlasRad - Modèle Utilisateur Personnalisé
Remplace le modèle User Django par défaut pour ajouter le champ "role".
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Utilisateur AtlasRad.
    Rôles:
    - 'user'  : Radiologue ou technicien (accès standard)
    - 'admin' : Administrateur de la plateforme (accès stats et gestion)
    """

    ROLE_CHOICES = [
        ('user', 'Utilisateur Standard'),
        ('admin', 'Administrateur Système'),
    ]

    # Champ role ajouté au modèle standard
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name="Rôle"
    )

    # Hôpital ou centre d'imagerie de rattachement
    hospital = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Hôpital / Centre"
    )

    # Spécialité médicale
    specialty = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Spécialité"
    )

    # Photo de profil (optionnelle)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Utilisateur AtlasRad"
        verbose_name_plural = "Utilisateurs AtlasRad"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin_role(self):
        """Vérification simplifiée si c'est un admin plateforme."""
        return self.role == 'admin'
