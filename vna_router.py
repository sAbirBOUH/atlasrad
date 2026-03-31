from pynetdicom import AE, evt, StoragePresentationContexts
from pydicom import dcmread
from pydicom.dataset import FileMetaDataset
import os
import pydicom

print("="*50)
print("📡 ATLASRAD - ROUTEUR VNA & ANONYMISEUR")
print("="*50)

# Dossier où on va sauvegarder les fichiers sécurisés
os.makedirs("dicom_anonymises", exist_ok=True)

def handle_store(event):
    """Fonction déclenchée quand un Scanner envoie une image DICOM"""
    dataset = event.dataset
    
    print("\n[INTERCEPTION] ⚠️ Nouvelle image DICOM reçue en plein vol !")
    # Afficher quelques infos originales
    nom_patient = dataset.get("PatientName", "Inconnu")
    modalite = dataset.get("Modality", "Inconnu")
    
    print(f"👉 Modalité : {modalite}")
    print(f"👉 Nom Original (Secret Médical) : {nom_patient}")
    
    # -------------------------------
    # ACTION VNA : ANONYMISATION
    # -------------------------------
    print("[AGENT] 🔄 Anonymisation des données en cours...")
    dataset.PatientName = "ANONYMIZED_ATLASRAD"
    dataset.PatientID = "AR-9999"
    dataset.PatientBirthDate = "19000101"
    
    # On ajoute les metadonnées pour pouvoir le sauvegarder proprement
    dataset.file_meta = event.file_meta
    
    # Sauvegarde sur le disque dur
    filename = f"dicom_anonymises/intercepte_{modalite}_{dataset.SOPInstanceUID}.dcm"
    dataset.save_as(filename, write_like_original=False)
    
    print(f"[SUCCÈS] ✅ Fichier sécurisé et routé vers : {filename}")
    print("-"*50)
    
    return 0x0000 # Code DICOM "Success" envoyé au scanner

# Configuration de notre Routeur VNA (Application Entity - SCP)
ae = AE(ae_title=b'ATLASRAD_VNA')

# On veut supporter tous les types de fichiers DICOM pour le stockage (CT, RM, CR, etc)
ae.supported_contexts = StoragePresentationContexts

# On écoute spécifiquement l'événement "C-STORE" (Quelqu'un sauvegarde vers nous)
handlers = [(evt.EVT_C_STORE, handle_store)]

print("⏳ Démarrage de l'écoute sur le port DICOM mondial (11112)...")
print("Branchez vos modalités sur ce port pour commencer le routage !")

# On démarre le serveur DICOM (blocking)
ae.start_server(('127.0.0.1', 11112), block=True, evt_handlers=handlers)
