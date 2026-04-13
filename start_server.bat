@echo off
title AtlasRad - Serveur Django
color 0B
echo.
echo  ╔══════════════════════════════════════╗
echo  ║   ATLASRAD - Démarrage Serveur       ║
echo  ║   Django REST Framework              ║
echo  ╚══════════════════════════════════════╝
echo.
echo  [►] Lancement du serveur sur http://127.0.0.1:8001
echo  [►] Admin panel : http://127.0.0.1:8001/admin/
echo.
echo  Appuyez sur CTRL+C pour arrêter le serveur.
echo.

cd /d "%~dp0"
python manage.py runserver 8001

pause
