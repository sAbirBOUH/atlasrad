import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

modal_html = """
    <!-- Demo Request Modal -->
    <div id="demoModal" class="hidden fixed inset-0 flex items-center justify-center bg-black/80 backdrop-blur-md transition-opacity" style="z-index: 9999;">
        <div class="bg-[#0B1E3D] border border-[#C5922A]/40 p-10 rounded-2xl w-full max-w-lg relative shadow-[0_0_50px_rgba(197,146,42,0.15)] transform transition-transform scale-100">
            <!-- Close button -->
            <button onclick="closeDemoModal()" class="absolute top-5 right-5 text-gray-400 hover:text-white transition-colors">
                <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[#1A6FA8] bg-[#1A6FA8]/10 text-[#00C8FF] text-xs font-bold mb-6 font-['Rajdhani'] tracking-widest uppercase">
                <span class="w-1.5 h-1.5 rounded-full bg-[#00C8FF] animate-pulse"></span>
                Secure Demo Request
            </div>
            
            <h2 class="text-3xl font-bold text-white mb-2 font-['Exo_2']">Débloquez l'IA Clinique</h2>
            <p class="text-gray-400 text-sm mb-8 leading-relaxed">Remplissez ce formulaire court. Un radiologue de notre équipe vous contactera pour tester l'agentivité AtlasRad dans votre architecture DICOM.</p>
            
            <form action="https://formspree.io/f/meepkeby" method="POST" class="flex flex-col gap-5">
                <div>
                    <label class="block text-xs font-semibold text-[#7A99BB] mb-1.5 uppercase tracking-wider">Nom Complet</label>
                    <input type="text" name="name" required placeholder="Dr. Sarah Sabir" class="w-full bg-[#040D1A]/80 border border-gray-700/50 rounded-lg px-4 py-3.5 text-white placeholder-gray-600 focus:outline-none focus:border-[#C5922A] focus:ring-1 focus:ring-[#C5922A] transition-all">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-[#7A99BB] mb-1.5 uppercase tracking-wider">Hôpital / Centre d'Imagerie</label>
                    <input type="text" name="hospital" required placeholder="CHU / Clinique X" class="w-full bg-[#040D1A]/80 border border-gray-700/50 rounded-lg px-4 py-3.5 text-white placeholder-gray-600 focus:outline-none focus:border-[#C5922A] focus:ring-1 focus:ring-[#C5922A] transition-all">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-[#7A99BB] mb-1.5 uppercase tracking-wider">Email Professionnel</label>
                    <input type="email" name="email" required placeholder="sarah@hopital.ma" class="w-full bg-[#040D1A]/80 border border-gray-700/50 rounded-lg px-4 py-3.5 text-white placeholder-gray-600 focus:outline-none focus:border-[#C5922A] focus:ring-1 focus:ring-[#C5922A] transition-all">
                </div>
                
                <button type="submit" class="mt-6 w-full bg-gradient-to-r from-[#C5922A] to-[#E8B856] text-[#040D1A] font-bold py-4 px-6 rounded-lg hover:shadow-[0_0_25px_rgba(197,146,42,0.4)] transition-all font-['Rajdhani'] tracking-wider uppercase text-lg group flex items-center justify-center gap-3">
                    Envoyer ma demande
                    <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                </button>
            </form>
        </div>
    </div>

    <script>
        function openDemoModal(e) {
            if(e) e.preventDefault();
            document.getElementById('demoModal').classList.remove('hidden');
            document.body.style.overflow = 'hidden'; // prevent scrolling
        }
        function closeDemoModal() {
            document.getElementById('demoModal').classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    </script>
</body>"""

# 1. Inject before </body>
html = html.replace("</body>", modal_html)

# 2. Add onclick to buttons
# Find Navbar CTA button "Réserver une Démo"
html = re.sub(r'(<button class="bg-white text-brand-950 px-6 py-2 rounded-full text-sm font-bold.*?)(">\s*Réserver une Démo\s*</button>)', 
              r'\1" onclick="openDemoModal(event)\2', html, flags=re.IGNORECASE)

# Find Hero Primary CTA "Discover Platform"
html = re.sub(r'(class="ar-btn-primary")', r'onclick="openDemoModal(event)" \1', html)

# Find Hero Secondary CTA "Request a Demo"
html = re.sub(r'(class="ar-btn-secondary")', r'onclick="openDemoModal(event)" \1', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Formspree modal and logic attached.")
