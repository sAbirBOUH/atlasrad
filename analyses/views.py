"""
AtlasRad - Views des Analyses Médicales

POST /api/analyses/upload   -> Upload image médicale
POST /api/analyses/analyze  -> Déclenche l'analyse IA (VRAI modèle)
GET  /api/analyses/history  -> Historique des analyses de l'utilisateur
GET  /api/analyses/dashboard/stats -> Stats globales (admin uniquement)
"""
import os
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Analysis
from .serializers import AnalysisUploadSerializer, AnalysisResultSerializer
from accounts.models import User
from .ai_engine import run_ai_analysis  # ← Vrai moteur IA (TorchXRayVision + MONAI)


# ─────────────────────────────────────────────
# ENDPOINT 1: Upload Image Médicale
# ─────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    """
    Upload d'une image médicale (JPEG, PNG ou DICOM simulé).
    Body (multipart/form-data):
        - image       : Fichier image
        - modality    : 'CT', 'MR', 'CR', 'US', etc.
        - description : Description de l'examen
        - patient_id  : ID patient anonymisé (optionnel)
    Retourne: L'ID de l'analyse créée à passer à /analyze
    """
    serializer = AnalysisUploadSerializer(data=request.data)
    if serializer.is_valid():
        analysis = serializer.save(user=request.user, status='pending')
        return Response({
            "error": False,
            "message": "Image uploadée avec succès. Lancez /analyze pour démarrer l'IA.",
            "analysis_id": analysis.id,
            "image_url": request.build_absolute_uri(analysis.image.url),
            "status": analysis.status,
        }, status=status.HTTP_201_CREATED)

    return Response({
        "error": True,
        "message": "Erreur d'upload.",
        "details": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────
# ENDPOINT 2: Analyser une Image (VRAI IA)
# ─────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_image(request):
    """
    Déclenche le VRAI moteur IA (TorchXRayVision + MONAI) sur une image uploadée.
    Body: { "analysis_id": 12 }
    """
    analysis_id = request.data.get('analysis_id')

    if not analysis_id:
        return Response({
            "error": True,
            "message": "analysis_id est requis. Uploadez d'abord l'image via /upload."
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        analysis = Analysis.objects.get(id=analysis_id, user=request.user)
    except Analysis.DoesNotExist:
        return Response({
            "error": True,
            "message": "Analyse introuvable ou non autorisée."
        }, status=status.HTTP_404_NOT_FOUND)

    if analysis.status == 'completed':
        return Response({
            "error": False,
            "message": "Cette analyse a déjà été traitée.",
            "analysis": AnalysisResultSerializer(analysis).data
        })

    # --- Mise à jour statut -> processing ---
    analysis.status = 'processing'
    analysis.save(update_fields=['status'])

    # --- Résolution du chemin absolu de l'image sur le disque ---
    image_path = os.path.join(settings.MEDIA_ROOT, str(analysis.image))

    # --- Appel du VRAI moteur IA (TorchXRayVision + MONAI) ---
    try:
        ai_result = run_ai_analysis(image_path, analysis.modality, analysis.description)
    except Exception as e:
        analysis.status = 'error'
        analysis.save(update_fields=['status'])
        return Response({
            "error": True,
            "message": f"Erreur du moteur IA: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # --- Sauvegarde des résultats en base ---
    analysis.ai_model = ai_result['ai_model']
    analysis.result = ai_result['result']
    analysis.confidence_score = ai_result['confidence_score']
    analysis.finding = ai_result['finding']
    analysis.status = 'completed'
    analysis.save()

    return Response({
        "error": False,
        "message": "Analyse IA terminée avec succès.",
        "analysis": AnalysisResultSerializer(analysis).data
    }, status=status.HTTP_200_OK)


# ─────────────────────────────────────────────
# ENDPOINT 3: Historique des Analyses
# ─────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    """
    Retourne l'historique des analyses de l'utilisateur connecté.

    Query params:
        ?limit=20       -> Nombre max de résultats (défaut: 20)
        ?status=...     -> Filtrer par statut (pending / completed / error)
        ?modality=CT    -> Filtrer par modalité
    """
    queryset = Analysis.objects.filter(user=request.user)

    status_filter = request.query_params.get('status')
    modality_filter = request.query_params.get('modality')
    limit = int(request.query_params.get('limit', 20))

    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if modality_filter:
        queryset = queryset.filter(modality=modality_filter.upper())

    analyses = queryset[:limit]

    return Response({
        "error": False,
        "count": queryset.count(),
        "analyses": AnalysisResultSerializer(analyses, many=True).data
    })


# ─────────────────────────────────────────────
# ENDPOINT 4: Dashboard Stats (Admin)
# ─────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Retourne les statistiques globales de la plateforme.
    Accessible uniquement aux administrateurs.
    """
    from django.utils import timezone
    from django.db.models import Count

    if request.user.role != 'admin' and not request.user.is_staff:
        return Response({
            "error": True,
            "message": "Accès refusé. Réservé aux administrateurs."
        }, status=status.HTTP_403_FORBIDDEN)

    today = timezone.now().date()

    total_analyses = Analysis.objects.count()
    total_users = User.objects.count()
    analyses_today = Analysis.objects.filter(created_at__date=today).count()
    completed_analyses = Analysis.objects.filter(status='completed').count()

    modality_breakdown = (
        Analysis.objects.values('modality')
        .annotate(count=Count('modality'))
        .order_by('-count')
    )

    recent = Analysis.objects.select_related('user').order_by('-created_at')[:5]

    return Response({
        "error": False,
        "stats": {
            "total_analyses": total_analyses,
            "total_users": total_users,
            "analyses_today": analyses_today,
            "completed_analyses": completed_analyses,
            "completion_rate": round((completed_analyses / total_analyses * 100) if total_analyses else 0, 1),
        },
        "modality_breakdown": list(modality_breakdown),
        "recent_analyses": AnalysisResultSerializer(recent, many=True).data
    })
