@echo off
title Test J.A.R.V.I.S.
echo ========================================
echo     Test rapide J.A.R.V.I.S.
echo ========================================
echo.

:: Activer l'environnement virtuel
if not exist "jarvis_env\Scripts\activate.bat" (
    echo ERREUR: Environnement virtuel non trouvé
    echo Lancez d'abord INSTALL_JARVIS.bat
    pause
    exit /b 1
)

call jarvis_env\Scripts\activate.bat

echo Test des modules principaux...

:: Créer un script de test temporaire
echo import sys > test_temp.py
echo import json >> test_temp.py
echo try: >> test_temp.py
echo     from modules.ollama_client import OllamaClient >> test_temp.py
echo     from modules.voice_manager import VoiceManager >> test_temp.py
echo     from modules.speech_recognition_module import SpeechRecognitionModule >> test_temp.py
echo     with open('config/config.json', 'r') as f: >> test_temp.py
echo         config = json.load(f) >> test_temp.py
echo     print('✅ Imports réussis') >> test_temp.py
echo     ollama = OllamaClient(config) >> test_temp.py
echo     print('✅ Client Ollama initialisé') >> test_temp.py
echo     response = ollama.get_response('Dis bonjour en français') >> test_temp.py
echo     print(f'✅ Test Ollama: {response[:50]}...') >> test_temp.py
echo except Exception as e: >> test_temp.py
echo     print(f'❌ Erreur: {e}') >> test_temp.py
echo     import traceback >> test_temp.py
echo     traceback.print_exc() >> test_temp.py

:: Exécuter le test
python test_temp.py

:: Nettoyer
del test_temp.py 2>nul

echo.
echo ========================================
echo Test terminé
echo ========================================
echo.
echo Si tout est OK, lancez START_JARVIS.bat
echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul