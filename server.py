# ==========================================
# ATLASRAD - Serveur Central (Backend IA)
# ==========================================
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import time

# 1. Création de l'application (Le Cerveau)
app = FastAPI(
    title="AtlasRad VNA API", 
    description="Moteur de routage DICOM et d'authentification clinique",
    version="1.0.0"
)

# 2. Autoriser notre site web (Frontend) à parler avec ce serveur
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En production, on mettra l'URL exacte du site Github
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Structure de données attendue pour la connexion
class LoginDemande(BaseModel):
    email: str
    password: str

# --- LES ROUTES (API ENDPOINTS) ---

@app.get("/")
def verifier_systeme():
    """Vérifie que le serveur est bien allumé"""
    return {
        "status": "online",
        "system": "AtlasRad - Cerveau Actif",
        "heure_serveur": time.time()
    }

@app.post("/api/login")
def connexion_clinique(demande: LoginDemande):
    """Vérifie l'identité du médecin dans notre base de données"""
    
    # Simulation d'une vérification sécurisée
    email_valide = "dr.sabir@chu-ibnrochd.ma"
    mdp_valide = "admin123"
    
    print(f"[AUTH] Tentative de connexion pour : {demande.email}")
    
    if demande.email == email_valide and demande.password == mdp_valide:
        print("[AUTH] Accès Autorisé. Génération du Token.")
        return {
            "token": "atlasrad_secure_token_98213",
            "message": "Bienvenue Dr. Sabir",
            "redirect": "/dashboard.html"
        }
    else:
        print("[AUTH] Accès Refusé. Identifiants incorrects.")
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")

# ==========================================
# Lancement du Serveur
# ==========================================
if __name__ == "__main__":
    print("="*50)
    print("🚀 DÉMARRAGE DU MOTEUR CENTRAL ATLASRAD...")
    print("🏥 Serveur en écoute sur le Réseau (Port 8000)")
    print("="*50)
    
    # Le serveur tourne en local sur la machine
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
