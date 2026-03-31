import re

with open("login.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace <form action="dashboard.html" method="GET" class="space-y-6">
# with <form id="loginForm" class="space-y-6">
html = html.replace('<form action="dashboard.html" method="GET" class="space-y-6">', '<form id="loginForm" class="space-y-6">')

# Modify the inputs to add id
html = html.replace('<input type="email" required', '<input type="email" id="emailInput" required')
html = html.replace('<input type="password" required', '<input type="password" id="passwordInput" required')

# Add an error message div before the button
error_div = """                <div id="errorMsg" class="hidden text-red-500 text-sm font-['Rajdhani'] uppercase tracking-widest font-bold text-center mt-2 p-3 bg-red-950/50 rounded-lg border border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.2)]">Identifiants incorrects ou serveur éteint.</div>
                <button type="submit" """
html = html.replace('<button type="submit" ', error_div)

# Add Javascript logic at the end of body
js_logic = """
    <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault(); // Empêche le chargement de la page
            
            const email = document.getElementById('emailInput').value;
            const password = document.getElementById('passwordInput').value;
            const btn = this.querySelector('button[type="submit"]');
            const errorMsg = document.getElementById('errorMsg');
            
            // État de chargement
            errorMsg.classList.add('hidden');
            const originalText = btn.innerHTML;
            btn.innerHTML = `<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline mt-0.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Vérification...`;
            
            try {
                // On va "frapper" à la Porte 8000
                const response = await fetch('http://127.0.0.1:8000/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email, password: password })
                });
                
                const data = await response.json();
                
                if(response.ok) {
                    // Le serveur a validé le mot de passe (Statut 200 OK)
                    btn.innerHTML = `<svg class="w-5 h-5 inline mr-2 text-[#040D1A]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Accès Autorisé !`;
                    btn.style.background = "#00FF9D";
                    btn.style.boxShadow = "0 0 25px rgba(0, 255, 157, 0.4)";
                    
                    // Sauvegarde une fausse preuve de connexion locale
                    localStorage.setItem('atlasrad_token', data.token);
                    
                    // On dirige gentiment le médecin vers le tableau de bord
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 800);
                } else {
                    // Le Python refuse (Mauvais identifiants)
                    errorMsg.innerText = "❌ " + (data.detail || 'Erreur de connexion');
                    errorMsg.classList.remove('hidden');
                    btn.innerHTML = originalText;
                }
                
            } catch (err) {
                // Le moteur Python est éteint (Serveur down !)
                errorMsg.innerText = "🔌 Erreur: Le moteur AtlasRad (Port 8000) semble éteint sur votre machine !";
                errorMsg.classList.remove('hidden');
                btn.innerHTML = originalText;
            }
        });
    </script>
</body>
"""

html = html.replace('</body>', js_logic)

with open("login.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Login patched with Fetch API")
