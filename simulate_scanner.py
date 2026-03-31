from pynetdicom import AE
from pydicom import Dataset
from pydicom.uid import generate_uid, ImplicitVRLittleEndian
import pydicom
import time

print("="*50)
print("🖥️  SIMULATEUR DE SCANNER (GE/SIEMENS)")
print("="*50)

print("\n1. Création d'une image DICOM Factice (Scanner Cérébral...)")

# On fabrique un DICOM à la volée
ds = Dataset()
ds.PatientName = "Mme. Khadija Benali" # Nom réel (sensible)
ds.PatientID = "CHU-49201"
ds.PatientBirthDate = "19650424"
ds.Modality = "CT"
ds.StudyDescription = "Scanner Cerebral Sans Injection"

# UIDs obligatoires pour que le fichier soit valide
ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.2" # CT Image Storage
ds.SOPInstanceUID = generate_uid()

file_meta = Dataset()
file_meta.TransferSyntaxUID = ImplicitVRLittleEndian
file_meta.MediaStorageSOPClassUID = ds.SOPClassUID
file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
file_meta.ImplementationClassUID = generate_uid()
ds.file_meta = file_meta

ds.is_little_endian = True
ds.is_implicit_VR = True

time.sleep(1)

# Étape 2: On envoie le fichier via le réseau DICOM vers AtlasRad
print("2. Début de la transmission réseau vers le Routeur AtlasRad (Port 11112)...")

ae = AE(ae_title=b'CT_SCANNER')
ae.add_requested_context(ds.SOPClassUID)

# Connexion au routeur (Association DICOM)
print("3. Association avec ATLASRAD_VNA...")
assoc = ae.associate('127.0.0.1', 11112, ae_title=b'ATLASRAD_VNA')

if assoc.is_established:
    print("  ✓ Association réussie !")
    print("4. Envoi de l'image (C-STORE)...")
    
    # Envoi de la donnée DICOM
    status = assoc.send_c_store(ds)
    
    if status and status.Status == 0x0000:
        print("\n✅ Transmission terminée. AtlasRad a bien reçu et intercepté l'image !")
    else:
        print("\n❌ AtlasRad a rejeté l'image.")
    
    assoc.release()
else:
    print("\n❌ Impossible de contacter le serveur AtlasRad. Est-ce que le script vna_router.py est allumé ?")
