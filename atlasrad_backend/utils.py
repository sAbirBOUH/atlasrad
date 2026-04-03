"""
AtlasRad - Gestion globale des erreurs et utilitaires
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """
    Handler d'erreurs personnalisé : retourne toujours un JSON uniforme.
    Format: { "error": true, "message": "...", "details": {...} }
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_payload = {
            "error": True,
            "status_code": response.status_code,
            "message": "",
            "details": response.data,
        }
        # On essaie d'extraire un message lisible
        if isinstance(response.data, dict):
            if "detail" in response.data:
                error_payload["message"] = str(response.data["detail"])
            else:
                error_payload["message"] = "Erreur de validation. Vérifiez les champs envoyés."
        else:
            error_payload["message"] = str(response.data)

        response.data = error_payload

    return response
