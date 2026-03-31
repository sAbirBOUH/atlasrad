# ==========================================
# ATLASRAD - Serveur Central (Backend IA)
# ==========================================
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import time
import sqlite3

# --- 0. INITIALISATION DE LA BASE DE DONNÉES SQLITE ---
def init_db():
    # Crée un fichier atlasrad.db automatiquement (la base de données)
    conn = sqlite3.connect("atlasrad.db")
    cursor = conn.cursor()
    
    # Création de la table des médecins (si elle n'existe pas encore)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medecins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # On ajoute au moins le compte Administrateur (Sabir) s'il n'y est pas
    cursor.execute("SELECT * FROM medecins WHERE email = 'sabir@atlasrad.com'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO medecins (nom, email, password, role)
            VALUES ('Sabir', 'sabir@atlasrad.com', 'admin123', 'Administrateur Système VNA')
        ''')
        print("[DATABASE] Compte Admin (Sabir) créé avec succès !")
    
    conn.commit()
    conn.close()

# Lancement de l'initialisation DB dès l'allumage du serveur
init_db()


# --- 1. CONFIGURATION DU MOTEUR FASTAPI ---
app = FastAPI(
    title="AtlasRad VNA API", 
    description="Moteur de routage DICOM et d'authentification clinique",
    version="1.0.0"
)

# Autorise notre HTML public à interagir avec le Cerveau (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginDemande(BaseModel):
    email: str
    password: str

# --- LES ROUTES (API ENDPOINTS) ---

@app.get("/")
def verifier_systeme():
    """Route pour vérifier que le port 8000 est bien vivant"""
    return {
        "status": "online",
        "system": "AtlasRad - Cerveau Actif",
        "database": "SQLite connectée",
        "heure_serveur": time.time()
    }

@app.post("/api/login")
def connexion_clinique(demande: LoginDemande):
    """Vérifie l'identité du médecin directement dans la base de données SQL"""
    print(f"[AUTH] Requête de connexion SQL pour : {demande.email}")
    
    # On se connecte à la DB "atlasrad.db"
    conn = sqlite3.connect("atlasrad.db")
    cursor = conn.cursor()
    
    # On cherche dans la table "medecins" une ligne avec le mail ET le mot de passe
    cursor.execute(
        "SELECT nom, role FROM medecins WHERE email = ? AND password = ?", 
        (demande.email, demande.password)
    )
    utilisateur = cursor.fetchone() # Fetchone() récupère la ligne trouvée (ou "None" si vide)
    conn.close()
    
    # Si "utilisateur" n'est pas vide = Le mot de passe est BON
    if utilisateur:
        nom_complet, role_user = utilisateur
        print(f"[AUTH] Accès Autorisé. Bonjour {nom_complet} ({role_user})")
        return {
            "token": "atlasrad_secure_token_98213",
            "message": f"Bienvenue {nom_complet}",
            "role": role_user,
            "redirect": "dashboard.html" # Indique à JavaScript (login.html) d'aller sur le Dashboard
        }
    else:
        # Si la ligne n'existe pas en DB, on rejette sèchement (Erreur 401)
        print("[AUTH] Accès Refusé. Identifiants incorrects.")
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")

# ==========================================
# Lancement du Serveur
# ==========================================
if __name__ == "__main__":
    print("="*50)
    print("🚀 DÉMARRAGE DU MOTEUR CENTRAL ATLASRAD...")
    print("💽 BASE DE DONNÉES (SQLite): CONNECTÉE")
    print("🏥 Serveur en écoute sur le Réseau (Port 8000)")
    print("="*50)
    
    # Le serveur tourne en local sur la machine
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
