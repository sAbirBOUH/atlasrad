# 🏥 AtlasRad Backend — API REST Django

Backend professionnel de la plateforme d'IA en radiologie **AtlasRad**.  
Stack : **Python 3.12 · Django 6 · Django REST Framework · JWT · SQLite**

---

## ⚡ Installation (5 minutes)

### 1. Installer les dépendances Python

```bash
pip install django djangorestframework djangorestframework-simplejwt Pillow python-dotenv django-cors-headers
```

### 2. Créer le fichier d'environnement

```bash
copy .env.example .env
# Ouvrez .env et changez SECRET_KEY si vous passez en production
```

### 3. Créer les tables en base de données

```bash
python manage.py makemigrations accounts analyses
python manage.py migrate
```

### 4. Créer un compte Administrateur

```bash
python manage.py createsuperuser
# Renseignez : username, email, mot de passe
# Puis allez dans http://127.0.0.1:8000/admin/ et changez le rôle → "admin"
```

### 5. Lancer le serveur

```bash
python manage.py runserver
# Ou double-cliquez sur start_server.bat
```

Le serveur est accessible sur : **http://127.0.0.1:8000**  
Interface Admin Django : **http://127.0.0.1:8000/admin/**

---

## 📡 Endpoints API

| Méthode | Route | Auth | Description |
|---------|-------|------|-------------|
| POST | `/api/auth/register/` | ❌ | Inscription |
| POST | `/api/auth/login/` | ❌ | Connexion → retourne JWT |
| POST | `/api/auth/token/refresh/` | ❌ | Renouveller le token |
| GET / PATCH | `/api/auth/me/` | ✅ JWT | Profil utilisateur |
| POST | `/api/analyses/upload/` | ✅ JWT | Upload image médicale |
| POST | `/api/analyses/analyze/` | ✅ JWT | Déclencher l'IA |
| GET | `/api/analyses/history/` | ✅ JWT | Historique analyses |
| GET | `/api/analyses/dashboard/stats/` | ✅ Admin | Statistiques globales |

---

## 🔑 Authentification

Toutes les routes (sauf register/login) nécessitent un header :
```
Authorization: Bearer <votre_access_token>
```

---

## 🧪 Exemple de requêtes

### Inscription
```json
POST /api/auth/register/
{
  "username": "sabir",
  "email": "sabir@atlasrad.com",
  "password": "SecurePass@123",
  "password_confirm": "SecurePass@123",
  "first_name": "Sabir",
  "hospital": "CHU Atlas",
  "specialty": "Radiologie"
}
```

### Connexion
```json
POST /api/auth/login/
{
  "username": "sabir",
  "password": "SecurePass@123"
}
// Réponse : { "tokens": { "access": "...", "refresh": "..." }, "user": {...} }
```

### Upload d'image + Analyse IA
```
1. POST /api/analyses/upload/  (multipart/form-data, champ "image")
   -> Retourne: { "analysis_id": 5 }

2. POST /api/analyses/analyze/
   Body: { "analysis_id": 5 }
   -> Retourne: résultat complet avec score de confiance
```

---

## 📁 Structure du Projet

```
ai-platform/
├── atlasrad_backend/       # Configuration Django
│   ├── settings.py         # Paramètres JWT, CORS, DB
│   ├── urls.py             # Routeur principal
│   └── utils.py            # Gestion erreurs globale
├── accounts/               # App Authentification & Utilisateurs
│   ├── models.py           # Modèle User (rôle, hôpital, spécialité)
│   ├── serializers.py      # Validation données
│   ├── views.py            # Register, Login, Profil
│   └── urls.py             # Routes /api/auth/
├── analyses/               # App Analyses IA
│   ├── models.py           # Modèle Analysis
│   ├── serializers.py      # Validation + formatage
│   ├── views.py            # Upload, Analyze (IA), History, Stats
│   └── urls.py             # Routes /api/analyses/
├── uploads/                # Images médicales uploadées (créé auto)
├── atlasrad.db             # Base de données SQLite
├── manage.py               # CLI Django
├── .env.example            # Variables d'environnement
└── AtlasRad_API_Postman.json # Collection Postman prête à l'emploi
```

---

## 🤖 Moteur IA (Simulation)

Le moteur sélectionne **automatiquement** le modèle IA selon la description DICOM :

| Mots-clés | Modèle IA |
|-----------|-----------|
| Cerebral / Brain / AVC / Stroke | MONAI Brain Tumor Segmentation v3.1 |
| Thorax / Poumon / Lung | LUNA16 Pulmonary Nodule Detection v2.8 |
| Abdomen / Foie / Rein | AbdomenSeg AI v1.5 |
| Coronaire / Aorte / Cardiaque | AortaSeg Cardiovascular v2.0 |
| Autres | AtlasRad General Analyzer v1.0 |

En production, remplacez la fonction `simulate_ai_analysis()` dans `analyses/views.py` par un vrai appel à un modèle MONAI ou TensorFlow Serving.

---

> **AtlasRad** — Construit pour la radiologie computationnelle du futur.
