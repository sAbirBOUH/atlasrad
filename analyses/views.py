"""
AtlasRad - Views des Analyses Médicales

POST /api/analyses/upload   -> Upload image médicale
POST /api/analyses/analyze  -> Déclenche l'analyse IA sur une image uploadée
GET  /api/analyses/history  -> Historique des analyses de l'utilisateur
GET  /api/analyses/dashboard/stats -> Stats globales (admin uniquement)
"""
import random
import os
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Analysis
from .serializers import AnalysisUploadSerializer, AnalysisResultSerializer
from accounts.models import User


# ─────────────────────────────────────────────
# MOTEUR IA - Simulation Clinique
# ─────────────────────────────────────────────

def simulate_ai_analysis(modality: str, description: str) -> dict:
    """
    Simule une analyse IA basée sur la modalité et la description de l'examen.
    En production, cette fonction appelle un vrai modèle (MONAI, TensorFlow, etc.)

    Retourne:
        - ai_model : Le modèle IA sélectionné automatiquement
        - result   : Résultat clinique
        - confidence_score : Score de confiance (%)
        - finding  : Description détaillée des findings
    """

    description_upper = description.upper()

    # --- Sélection automatique du modèle IA en fonction de la description ---
    if any(k in description_upper for k in ['CEREBR', 'BRAIN', 'CRAN', 'AVC', 'STROKE', 'NEURO']):
        ai_model = "MONAI Brain Tumor Segmentation v3.1"
        findings_pool = [
            ("No significant intracranial abnormality detected.", 97.2,
             "Pas de lésion expansive, d'hémorragie ou d'ischémie identifiable. Structures médianes en place. Système ventriculaire de taille normale."),
            ("Possible ischemic lesion - Right temporal lobe.", 89.4,
             "Zone d'hypersignal FLAIR du lobe temporal droit mesurant 12x8mm, compatible avec une plage d'ischémie récente. Recommandation: IRM de contrôle à 48-72h."),
            ("Mass effect detected - Frontal region.", 94.1,
             "Processus expansif frontal gauche avec effet de masse modéré sur la corne frontale. Œdème périlésionnel. Investigation complémentaire (spectro-IRM, TEP) recommandée."),
        ]

    elif any(k in description_upper for k in ['THORAX', 'POUMON', 'LUNG', 'PULM', 'THORAC']):
        ai_model = "LUNA16 Pulmonary Nodule Detection v2.8"
        findings_pool = [
            ("No pulmonary nodules detected.", 96.7,
             "Parenchyme pulmonaire d'aspect normal. Pas de nodule, d'opacité ou de masse identifiable. Médiastin de contours réguliers. Pas d'épanchement pleural."),
            ("Suspicious nodule detected - Right lower lobe.", 82.3,
             "Nodule sous-solide de 8mm dans le lobe inférieur droit (segment 9). Score Lung-RADS: 3. Recommandation: TDM de contrôle à 6 mois."),
            ("Ground-glass opacity - COVID-19 pattern possible.", 88.5,
             "Opacités en verre dépoli bilatérales à prédominance périphérique et postérieure, compatible avec une pneumopathie virale. Corrélation clinique et biologique recommandée."),
        ]

    elif any(k in description_upper for k in ['ABDOMEN', 'FOIE', 'LIVER', 'REIN', 'HEPAT', 'ABDO']):
        ai_model = "AbdomenSeg AI v1.5"
        findings_pool = [
            ("No significant abdominal pathology.", 95.8,
             "Foie de taille et échogénicité normales. Rate, pancréas et reins sans particularité. Pas d'épanchement intra-péritonéal."),
            ("Liver lesion detected - Segment VII.", 87.9,
             "Lésion hépatique kystique de 22mm en segment VII (S7), à parois fines, sans septa ni vascularisation interne. Aspect benin, compatible avec un kyste simple."),
        ]

    elif any(k in description_upper for k in ['CARDIOVASC', 'CORON', 'AORTE', 'AORT', 'CARDIAC']):
        ai_model = "AortaSeg Cardiovascular v2.0"
        findings_pool = [
            ("No coronary stenosis detected (CAC-RADS 0).", 99.1,
             "Score calcique coronarien (Agatston): 0. Aucune calcification coronarienne identifiée. Risque cardiovasculaire très faible."),
            ("Mild aortic calcification noted.", 91.5,
             "Calcifications athéromateuses de l'aorte abdominale sans dilatation anévrismale (diamètre max: 34mm en sous-rénal). Suivi annuel recommandé."),
        ]

    else:
        # Modèle généraliste par défaut
        ai_model = "AtlasRad General Analyzer v1.0"
        findings_pool = [
            ("No significant abnormality detected.", 93.5, "Examen dans les limites de la normale pour la modalité et l'indication clinique."),
            ("Minor findings - Clinical correlation recommended.", 78.2, "Quelques anomalies mineures identifiées. Une corrélation clinique et un suivi à 3 mois sont conseillés."),
        ]

    # Sélection aléatoire d'un résultat dans le pool (simulation)
    result_text, confidence, finding = random.choice(findings_pool)

    # Légère variation du score de confiance pour simuler un vrai modèle
    confidence = round(confidence + random.uniform(-2.0, 2.0), 1)

    return {
        "ai_model": ai_model,
        "result": result_text,
        "confidence_score": max(75.0, min(99.9, confidence)),
        "finding": finding,
    }


# ─────────────────────────────────────────────
# ENDPOINT 1: Upload Image Médicale
# ─────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    """
    Upload d'une image médicale (JPEG, PNG ou DICOM simulé).
    L'image est stockée côté serveur et associée à l'utilisateur.

    Body (multipart/form-data):
        - image     : Fichier image
        - modality  : 'CT', 'MR', 'CR', 'US', etc.
        - description : Description de l'examen (ex: "Scanner Thorax")
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
# ENDPOINT 2: Analyser une Image
# ─────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_image(request):
    """
    Déclenche la simulation du moteur IA sur une image déjà uploadée.

    Body: { "analysis_id": 12 }
    Retourne: résultat complet de l'analyse
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

    # --- Appel du moteur IA (simulation) ---
    ai_result = simulate_ai_analysis(analysis.modality, analysis.description)

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

    # Filtres optionnels
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

    Retourne:
        - total_analyses : Nombre total d'analyses
        - total_users    : Nombre d'utilisateurs inscrits
        - analyses_today : Analyses effectuées aujourd'hui
        - recent_analyses : Les 5 dernières analyses
        - modality_breakdown : Répartition par modalité
    """
    from django.utils import timezone
    from django.db.models import Count

    # Vérification du rôle admin
    if request.user.role != 'admin' and not request.user.is_staff:
        return Response({
            "error": True,
            "message": "Accès refusé. Réservé aux administrateurs."
        }, status=status.HTTP_403_FORBIDDEN)

    today = timezone.now().date()

    # Stats globales
    total_analyses = Analysis.objects.count()
    total_users = User.objects.count()
    analyses_today = Analysis.objects.filter(created_at__date=today).count()
    completed_analyses = Analysis.objects.filter(status='completed').count()

    # Répartition par modalité
    modality_breakdown = (
        Analysis.objects.values('modality')
        .annotate(count=Count('modality'))
        .order_by('-count')
    )

    # Dernières analyses (avec infos utilisateur)
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
