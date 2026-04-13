"""
Script de diagnostic complet de l'API AtlasRad upload.
Lance avec: python diagnose_upload.py
"""
import os
import io
import sys
import json
import requests
from PIL import Image

BASE = "http://127.0.0.1:8001"

# ── 1. Login ──────────────────────────────
print("1. Login...")
r = requests.post(f"{BASE}/api/auth/login/", json={"username": "sabir", "password": "AtlasPass@123"})
print(f"   Status: {r.status_code}")
print(f"   Body:   {r.text[:300]}")

if r.status_code != 200:
    print("\nLOGIN FAILED. Essayons de créer l'utilisateur...")
    r2 = requests.post(f"{BASE}/api/auth/register/", json={
        "username": "sabir",
        "email": "sabir@atlasrad.com",
        "password": "AtlasPass@123",
        "password_confirm": "AtlasPass@123",
        "first_name": "Sabir",
        "last_name": "Admin"
    })
    print(f"   Register status: {r2.status_code} — {r2.text[:200]}")
    sys.exit(1)

token = r.json()["tokens"]["access"]
print(f"   Token OK: {token[:40]}...")

# ── 2. Créer une image test PNG en mémoire ─
print("\n2. Création d'une image test...")
img = Image.new("RGB", (224, 224), color=(128, 128, 128))
buf = io.BytesIO()
img.save(buf, format="JPEG")
buf.seek(0)

# ── 3. Upload ────────────────────────────
print("\n3. Test upload...")
r3 = requests.post(
    f"{BASE}/api/analyses/upload/",
    headers={"Authorization": f"Bearer {token}"},
    files={"image": ("test_chest.jpg", buf, "image/jpeg")},
    data={
        "modality": "CR",
        "description": "Radiographie Thorax Test",
        "patient_id": "TEST-001"
    }
)
print(f"   Status: {r3.status_code}")
print(f"   Body:   {json.dumps(r3.json(), indent=2, ensure_ascii=False)}")

if r3.status_code != 201:
    print("\nUPLOAD FAILED. Problème identifié ci-dessus.")
    sys.exit(1)

analysis_id = r3.json()["analysis_id"]
print(f"   analysis_id = {analysis_id}")

# ── 4. Analyze ───────────────────────────
print("\n4. Test analyse IA...")
r4 = requests.post(
    f"{BASE}/api/analyses/analyze/",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"analysis_id": analysis_id}
)
print(f"   Status: {r4.status_code}")
print(f"   Body:   {json.dumps(r4.json(), indent=2, ensure_ascii=False)}")

print("\nDIAGNOSTIC TERMINE.")
