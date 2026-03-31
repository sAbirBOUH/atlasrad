import sqlite3
import re

# 1. Update server.py
with open("server.py", "r", encoding="utf-8") as f:
    server_code = f.read()

new_table_sql = '''
    # Création de la table des examens médicaux interceptés
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS examens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anonymized_id TEXT,
            modalite TEXT,
            description TEXT,
            modele_ia TEXT,
            statut TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
'''
server_code = server_code.replace("    conn.commit()\n    conn.close()", new_table_sql + "    conn.close()")

new_endpoint = '''
@app.get("/api/exams")
def get_exams():
    """Récupère la liste des examens DICOM depuis la base de données SQLite"""
    conn = sqlite3.connect("atlasrad.db")
    cursor = conn.cursor()
    cursor.execute("SELECT anonymized_id, modalite, description, modele_ia, statut FROM examens ORDER BY id DESC LIMIT 10")
    lignes = cursor.fetchall()
    conn.close()
    
    result = []
    for l in lignes:
        result.append({"id": l[0], "modalite": l[1], "description": l[2], "ia": l[3], "statut": l[4]})
    return {"examens": result}

# ==========================================
'''
server_code = server_code.replace("# ==========================================\n# Lancement du Serveur", new_endpoint + "# Lancement du Serveur")

with open("server.py", "w", encoding="utf-8") as f:
    f.write(server_code)


# 2. Update vna_router.py
with open("vna_router.py", "r", encoding="utf-8") as f:
    router_code = f.read()

db_insert_code = '''
    import sqlite3
    try:
        conn = sqlite3.connect("atlasrad.db")
        cursor = conn.cursor()
        
        # Le "Cerveau" attribue automatiquement un Agent IA selon la description DICOM
        ia_attribue = "Analyse Générique standard"
        desc = dataset.get("StudyDescription", "Inconnu").upper()
        if "CEREBRAL" in desc or "BRAIN" in desc or "CRA" in desc:
            ia_attribue = "MONAI Brain Tumor 🧠"
        elif "THORAX" in desc or "POUMON" in desc:
            ia_attribue = "LUNA16 (Poumon) 🫁"
            
        # Insertion dans la vraie table de la plateforme
        cursor.execute("""
            INSERT INTO examens (anonymized_id, modalite, description, modele_ia, statut)
            VALUES (?, ?, ?, ?, ?)
        """, ("AR-9999", modalite, dataset.get("StudyDescription", "Inconnu"), ia_attribue, "Anonymisé & Routé"))
        conn.commit()
        conn.close()
        print("[DATABASE] 📝 Ligne interceptée et ajoutée visiblement sur le Tableau de Bord ! !")
    except Exception as e:
        print(f"[ERREUR DB] {e}")
        
    print(f"[SUCCÈS] ✅ Fichier sécurisé et routé vers : {filename}")
'''
router_code = router_code.replace('print(f"[SUCCÈS] ✅ Fichier sécurisé et routé vers : {filename}")', db_insert_code)

with open("vna_router.py", "w", encoding="utf-8") as f:
    f.write(router_code)


# 3. Update dashboard.html
with open("dashboard.html", "r", encoding="utf-8") as f:
    dash_code = f.read()

# Replace the fake hardcoded HTML lines in the table with an empty tbody
dash_code = re.sub(r'<tbody id="vna-queue">.*?</tbody>', '<tbody id="vna-queue"></tbody>', dash_code, flags=re.DOTALL)

# Inject JS to pull data every 2 seconds
fetch_js = '''
        // Fetch les vrais examens depuis le Cerveau (server.py)
        async function fetchExams() {
            try {
                const res = await fetch('http://127.0.0.1:8000/api/exams');
                const data = await res.json();
                const tbody = document.getElementById('vna-queue');
                tbody.innerHTML = ''; // On efface pour mettre à jour
                
                data.examens.forEach(ex => {
                    let statusColor = ex.statut.includes("Anonymisé") ? "#00FF9D" : "#E8B856";
                    let animClass = ex.statut.includes("Anonymisé") ? "" : "animate-pulse";
                    
                    let tr = document.createElement('tr');
                    tr.classList.add("border-b", "border-[#1A6FA8]/20", "hover:bg-[#1A6FA8]/10", "transition-colors");
                    tr.innerHTML = `
                        <td class="font-mono text-[#00C8FF] font-bold p-4 py-3">${ex.id}</td>
                        <td class="p-4 py-3"><span class="bg-gray-800 text-xs px-2 py-1 rounded font-bold border border-gray-600">${ex.modalite}</span></td>
                        <td class="text-sm p-4 py-3">${ex.description}</td>
                        <td class="text-sm font-semibold text-[#1A6FA8] p-4 py-3">${ex.ia}</td>
                        <td class="p-4 py-3">
                            <div class="flex items-center gap-2">
                                <span class="w-2 h-2 rounded-full ${animClass}" style="background:${statusColor}; box-shadow: 0 0 10px ${statusColor}"></span> 
                                <span class="text-xs font-bold" style="color:${statusColor}">${ex.statut}</span>
                            </div>
                        </td>
                        <td class="p-4 py-3"><button class="text-xs font-bold bg-[#1A6FA8]/20 px-3 py-1 rounded border border-[#1A6FA8] text-[#00C8FF] hover:bg-[#1A6FA8] hover:text-white uppercase transition-all">Ouvrir</button></td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch(e) {
                console.error("API non détectée : Le serveur Python est-il allumé sur le port 8000 ?", e);
            }
        }
        
        // Rafraîchissement automatique de la liste toutes les 2 secondes (Live Feed)
        setInterval(fetchExams, 2000);
        fetchExams();
'''

dash_code = dash_code.replace("setTimeout(appendLog, 1500);", "setTimeout(appendLog, 1500);\n\n" + fetch_js)

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(dash_code)

print("Pont DICOM -> Base de données -> Dashboard créé et raccordé !")
