"""
AtlasRad - Serializers des Analyses Médicales
"""
from rest_framework import serializers
from .models import Analysis


class AnalysisUploadSerializer(serializers.ModelSerializer):
    """Serializer pour l'upload d'une nouvelle image médicale."""

    class Meta:
        model = Analysis
        fields = ['id', 'image', 'modality', 'description', 'patient_id']

    def validate_image(self, value):
        """Validation de l'image : taille max 20MB, formats autorisés."""
        max_size = 20 * 1024 * 1024  # 20 MB
        if value.size > max_size:
            raise serializers.ValidationError("Image trop volumineuse. Limite: 20MB.")

        allowed_types = ['image/jpeg', 'image/png', 'image/dicom', 'application/octet-stream']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Format non supporté. Accepté: JPEG, PNG, DICOM.")

        return value


class AnalysisResultSerializer(serializers.ModelSerializer):
    """Serializer complet avec résultats IA pour l'historique et l'affichage."""

    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Analysis
        fields = [
            'id', 'user_name', 'modality', 'description', 'patient_id',
            'ai_model', 'result', 'confidence_score', 'finding',
            'status', 'image', 'created_at'
        ]
        read_only_fields = fields

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
