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
python -c "
try:
    from modules.ollama_client import OllamaClient
    from modules.voice_manager import VoiceManager
    from modules.speech_recognition_module import SpeechRecognitionModule
    import json
    
    # Charger la config
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    
    print('✅ Imports réussis')
    
    # Test Ollama
    ollama = OllamaClient(config)
    print('✅ Client Ollama initialisé')
    
    # Test simple
    response = ollama.get_response('Dis bonjour en français')
    print(f'✅ Test Ollama: {response[:50]}...')
    
except Exception as e:
    print(f'❌ Erreur: {e}')
    import traceback
    traceback.print_exc()
"

echo.
echo ========================================
echo Test terminé
echo ========================================
echo.
echo Si tout est OK, lancez START_JARVIS.bat
echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul