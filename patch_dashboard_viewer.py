import re

with open("dashboard.html", "r", encoding="utf-8") as f:
    dash_code = f.read()

# 1. Add the Report Modal HTML just before </body>
report_modal_html = """
    <!-- AI Report & Viewer Modal -->
    <div id="reportModal" class="hidden fixed inset-0 flex items-center justify-center bg-black/90 backdrop-blur-xl transition-opacity" style="z-index: 9999;">
        <div class="bg-[#040D1A] border border-[#1A6FA8]/50 rounded-xl w-[95vw] max-w-7xl h-[90vh] flex flex-col shadow-[0_0_80px_rgba(26,111,168,0.2)] overflow-hidden transform scale-100 transition-transform">
            
            <!-- Header -->
            <div class="h-16 border-b border-[#1A6FA8]/30 flex items-center justify-between px-6 bg-[#0B1E3D]">
                <div class="flex items-center gap-4">
                    <div class="px-3 py-1 bg-[#C5922A]/20 border border-[#C5922A] text-[#E8B856] text-xs font-bold rounded uppercase tracking-widest font-['Rajdhani']">
                        URGENCE CRITIQUE
                    </div>
                    <h2 class="text-xl font-bold font-['Exo_2'] text-white"><span id="reportModalID">AR-9999</span> | <span id="reportModalDesc">CT Scanner Cerebral</span></h2>
                </div>
                
                <div class="flex items-center gap-4">
                    <div class="text-[#00C8FF] text-xs font-mono bg-[#1A6FA8]/10 px-3 py-1 rounded border border-[#1A6FA8]/30">
                        Analyzed by: <span id="reportModalIA" class="font-bold text-white">MONAI Brain Tumor</span>
                    </div>
                    <button onclick="closeReportModal()" class="text-gray-400 hover:text-white p-2 rounded-lg hover:bg-white/10 transition-colors">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                </div>
            </div>

            <!-- Content Area -->
            <div class="flex-1 flex overflow-hidden">
                
                <!-- Left: Fake Zero-Footprint Viewer (OHIF style) -->
                <div class="flex-1 border-r border-[#1A6FA8]/30 bg-black relative flex flex-col">
                    <div class="h-10 bg-gray-900 border-b border-gray-800 flex items-center px-4 gap-4 text-gray-400">
                        <svg class="w-5 h-5 hover:text-white cursor-pointer" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                        <svg class="w-5 h-5 hover:text-white cursor-pointer" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"></path></svg>
                        <svg class="w-5 h-5 hover:text-white cursor-pointer" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                        <div class="ml-auto text-xs font-mono">WW: 80 WL: 40</div>
                    </div>
                    
                    <div class="flex-1 relative overflow-hidden flex items-center justify-center">
                        <div class="absolute top-4 left-4 text-xs font-mono text-gray-500">
                            Dr. Sabir (AtlasRad)<br>
                            DOB: 19XX-XX-XX<br>
                            Seq: 3/4<br>
                            Slice: <span class="text-white">45</span>/120
                        </div>
                        <div class="absolute bottom-4 right-4 text-xs font-mono text-gray-500 text-right">
                            Thickness: 1.0mm<br>
                            FoV: 240mm<br>
                            <span class="text-[#E8B856]">AI Overlay: ON</span>
                        </div>
                        
                        <!-- Simulated Brain MRI with heatmap (CSS drawing) -->
                        <div class="w-64 h-80 rounded-[40%] bg-gradient-to-b from-gray-300 via-gray-400 to-gray-600 opacity-80 blur-sm flex items-center justify-center relative">
                            <!-- Ventricles -->
                            <div class="w-16 h-24 bg-gray-900 rounded-[50%] absolute top-1/4"></div>
                            <!-- Tumor Overlay -->
                            <div class="absolute top-[35%] right-[20%] w-16 h-16 rounded-full bg-red-500/50 blur-md animate-pulse border-2 border-red-500 border-dashed"></div>
                            <div class="absolute top-[35%] right-[20%] w-16 h-16 rounded-full border border-red-500 flex items-center justify-center shadow-[0_0_15px_rgba(239,68,68,0.8)]">
                                <svg class="w-full h-full text-red-500 opacity-50" viewBox="0 0 100 100"><line x1="0" y1="50" x2="100" y2="50" stroke="currentColor" stroke-width="1"/><line x1="50" y1="0" x2="50" y2="100" stroke="currentColor" stroke-width="1"/></svg>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right: Structured AI Report -->
                <div class="w-full md:w-[450px] bg-[#02050B] p-8 flex flex-col overflow-y-auto">
                    <h3 class="text-[#7A99BB] uppercase tracking-widest text-xs font-bold mb-6 border-b border-gray-800 pb-2">Rapport Médical Agentique</h3>
                    
                    <div class="space-y-6 flex-1">
                        <div>
                            <div class="text-xs text-gray-500 mb-1 font-mono">Confiance du Modèle</div>
                            <div class="flex items-center gap-3">
                                <div class="text-3xl font-bold text-white font-['Rajdhani']">98.4%</div>
                                <div class="h-2 flex-1 bg-gray-800 rounded-full overflow-hidden">
                                    <div class="h-full bg-gradient-to-r from-[#C5922A] to-red-500 w-[98%]"></div>
                                </div>
                            </div>
                        </div>

                        <div class="bg-[#1A6FA8]/10 border border-[#1A6FA8]/30 rounded-lg p-4">
                            <div class="text-[#00C8FF] text-sm font-bold mb-2 flex items-center gap-2">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                Découvertes Clés (Findings)
                            </div>
                            <p class="text-gray-300 text-sm leading-relaxed mb-3">
                                Massif tissulaire hyperdense détecté dans le lobe frontal droit, mesurant environ <span class="text-white font-bold bg-red-500/20 px-1">4.2 x 3.1 x 3.8 cm</span> (Volume: 25.4 cc). Edème péritumoral vasogénique modéré causant un effet de masse sur la corne frontale du ventricule latéral droit.
                            </p>
                            <p class="text-gray-300 text-sm leading-relaxed">
                                Pas d'engagement sous-falciforme sévère. Reste du parenchyme cérébral sans anomalie focale aiguë.
                            </p>
                        </div>
                        
                        <div>
                            <div class="text-[#7A99BB] text-xs font-bold uppercase mb-2">Impression Diagnostique</div>
                            <ul class="list-disc pl-5 text-sm text-gray-300 space-y-1">
                                <li>Lésion expansive frontale droite fortement suspecte (Glioblastome vs Métastase).</li>
                                <li>Effet de masse modéré.</li>
                            </ul>
                        </div>
                    </div>

                    <!-- Actions -->
                    <div class="mt-8 pt-6 border-t border-gray-800 flex flex-col gap-3">
                        <button class="w-full bg-[#00FF9D]/20 border border-[#00FF9D] text-[#00FF9D] hover:bg-[#00FF9D] hover:text-black font-bold py-3 rounded-lg transition-colors flex justify-center items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                            Valider le rapport (Sign)
                        </button>
                        <div class="flex gap-3">
                            <button class="flex-1 bg-red-500/10 border border-red-500/50 text-red-500 font-bold py-2 rounded-lg text-sm hover:bg-red-500 hover:text-white transition-colors">
                                Faux Positif
                            </button>
                            <button class="flex-1 bg-[#1A6FA8]/20 border border-[#1A6FA8]/50 text-[#00C8FF] font-bold py-2 rounded-lg text-sm hover:bg-[#1A6FA8] hover:text-white transition-colors">
                                Exporter PDF
                            </button>
                        </div>
                    </div>
                </div>
                
            </div>
        </div>
    </div>
"""

# Inject before </body>
dash_code = dash_code.replace("</body>", report_modal_html + "\n</body>")

# 2. Modify the fetchExams logic to attach the onClick handler to the "Ouvrir" button
# We replace the button HTML to include onclick
button_search = r'<td class="p-4 py-3"><button class="text-xs font-bold bg-\[#1A6FA8\]/20 px-3 py-1 rounded border border-\[#1A6FA8\] text-\[#00C8FF\] hover:bg-\[#1A6FA8\] hover:text-white uppercase transition-all">Ouvrir</button></td>'
button_replace = r'<td class="p-4 py-3"><button onclick="openReportModal(\'${ex.id}\', \'${ex.description}\', \'${ex.ia}\')" class="text-xs font-bold bg-[#1A6FA8]/20 px-3 py-1 rounded border border-[#1A6FA8] text-[#00C8FF] hover:bg-[#1A6FA8] hover:text-white hover:shadow-[0_0_15px_rgba(0,200,255,0.4)] uppercase transition-all">Ouvrir Dossier</button></td>'

dash_code = dash_code.replace(button_search, button_replace)

# 3. Add JS functions for open/close Modal
modal_js = """
        function openReportModal(id, desc, ia) {
            document.getElementById('reportModalID').innerText = "EXAM-" + id;
            document.getElementById('reportModalDesc').innerText = desc || "Scanner Medical";
            document.getElementById('reportModalIA').innerText = ia || "AtlasRad Agent";
            document.getElementById('reportModal').classList.remove('hidden');
        }
        function closeReportModal() {
            document.getElementById('reportModal').classList.add('hidden');
        }
"""
dash_code = dash_code.replace("</script>", modal_js + "\n    </script>")

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(dash_code)

print("Viewer and AI Report Modal generated & injected successfully!")
