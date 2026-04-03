"""
AtlasRad - Model des Analyses Médicales
"""
from django.db import models
from django.conf import settings


class Analysis(models.Model):
    """
    Représente une analyse IA d'une image médicale.
    Chaque analyse est liée à un utilisateur (radiologue).
    """

    MODALITY_CHOICES = [
        ('CT', 'Scanner CT'),
        ('MR', 'IRM / MRI'),
        ('CR', 'Radiographie'),
        ('US', 'Échographie'),
        ('PT', 'PET Scan'),
        ('OTHER', 'Autre'),
    ]

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processing', 'En cours de traitement'),
        ('completed', 'Terminé'),
        ('error', 'Erreur'),
    ]

    # Lien vers l'utilisateur qui a soumis l'analyse
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analyses',
        verbose_name="Radiologue"
    )

    # Image médicale uploadée
    image = models.ImageField(
        upload_to='medical_images/%Y/%m/',
        verbose_name="Image médicale"
    )

    # Informations sur l'examen
    modality = models.CharField(
        max_length=10,
        choices=MODALITY_CHOICES,
        default='CT',
        verbose_name="Modalité"
    )
    description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Description de l'examen"
    )
    patient_id = models.CharField(
        max_length=50,
        blank=True,
        default='ANONYMIZED',
        verbose_name="ID Patient (Anonymisé)"
    )

    # Résultats de l'IA
    ai_model = models.CharField(
        max_length=100,
        default='AtlasRad General v1.0',
        verbose_name="Modèle IA utilisé"
    )
    result = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Résultat IA"
    )
    confidence_score = models.FloatField(
        default=0.0,
        verbose_name="Score de confiance (%)"
    )
    finding = models.TextField(
        blank=True,
        verbose_name="Description des findings"
    )

    # Statut du traitement
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Statut"
    )

    # Horodatage
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'analyse")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Analyse IA"
        verbose_name_plural = "Analyses IA"

    def __str__(self):
        return f"[{self.modality}] {self.patient_id} - {self.result or 'En attente'}"
