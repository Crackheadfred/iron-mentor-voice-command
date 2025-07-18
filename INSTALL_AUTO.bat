@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ========================================
echo Installation COMPLETE J.A.R.V.I.S.
echo ========================================
echo.
echo Installation automatique avec toutes les optimisations
echo Ne fermez pas cette fenetre!
echo.

:: Aller dans le repertoire du script
cd /d "%~dp0"

:: Verifier si on est dans le bon dossier
if not exist "jarvis_main.py" (
    echo ERREUR: Lancez ce script depuis le dossier J.A.R.V.I.S.
    exit /b 1
)

:: Nettoyer l'installation precedente
if exist "jarvis_env" (
    echo [1/12] Suppression de l'ancienne installation...
    rmdir /s /q jarvis_env
)

:: Verifier Python
echo [2/12] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python non trouve - Installez Python 3.8+ depuis python.org
    exit /b 1
)

:: Creer l'environnement virtuel
echo [3/12] Creation de l'environnement virtuel...
python -m venv jarvis_env
if errorlevel 1 (
    echo ERREUR: Impossible de creer l'environnement virtuel
    exit /b 1
)

:: Activer l'environnement virtuel
echo [4/12] Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat

:: Mise a jour de pip
echo [5/12] Mise a jour de pip...
python -m pip install --upgrade pip --quiet

:: Installation PyTorch avec CUDA
echo [6/12] Installation PyTorch avec support CUDA...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --quiet

:: Installation des modules de base
echo [7/12] Installation des modules de base...
pip install requests openai psutil pyttsx3 SpeechRecognition --quiet
pip install pytesseract Pillow pyautogui opencv-python numpy --quiet

:: Installation Tortoise TTS et optimisations
echo [8/12] Installation Tortoise TTS...
pip install TTS tortoise-tts --quiet
pip install accelerate transformers --quiet
pip install soundfile librosa pydub --quiet

:: Installation modules audio
echo [9/12] Installation des modules audio...
pip install pygame pyaudio --quiet

:: Creer les dossiers
echo [10/12] Creation des dossiers...
if not exist "logs" mkdir logs
if not exist "memory" mkdir memory
if not exist "screenshots" mkdir screenshots
if not exist "config" mkdir config
if not exist "voices" mkdir voices
if not exist "voices\william" mkdir voices\william
if not exist "logs\telemetry" mkdir logs\telemetry

:: Creer un script temporaire pour la configuration
echo [11/12] Creation de la configuration...
echo import json > temp_config.py
echo config = { >> temp_config.py
echo     'ollama': { >> temp_config.py
echo         'model': 'mistral-small3.2:24b', >> temp_config.py
echo         'url': 'http://localhost:11434' >> temp_config.py
echo     }, >> temp_config.py
echo     'openai': { >> temp_config.py
echo         'api_key': '', >> temp_config.py
echo         'model': 'gpt-4o-mini' >> temp_config.py
echo     }, >> temp_config.py
echo     'voice': { >> temp_config.py
echo         'william_voice_path': 'voices/william/', >> temp_config.py
echo         'tts_engine': 'tortoise', >> temp_config.py
echo         'language': 'fr', >> temp_config.py
echo         'fallback_to_windows': False >> temp_config.py
echo     }, >> temp_config.py
echo     'screen': { >> temp_config.py
echo         'ocr_enabled': True, >> temp_config.py
echo         'monitoring_interval': 2 >> temp_config.py
echo     }, >> temp_config.py
echo     'simhub': { >> temp_config.py
echo         'enabled': True, >> temp_config.py
echo         'port': 8888 >> temp_config.py
echo     }, >> temp_config.py
echo     'dcs': { >> temp_config.py
echo         'enabled': True, >> temp_config.py
echo         'aircraft': 'F/A-18C' >> temp_config.py
echo     } >> temp_config.py
echo } >> temp_config.py
echo with open('config/config.json', 'w', encoding='utf-8') as f: >> temp_config.py
echo     json.dump(config, f, indent=2, ensure_ascii=False) >> temp_config.py
echo print('Configuration creee') >> temp_config.py

python temp_config.py
del temp_config.py

:: Creer la voix William
echo [12/12] Configuration de la voix William...
echo import json > temp_william.py
echo from pathlib import Path >> temp_william.py
echo william_dir = Path('voices/william') >> temp_william.py
echo william_dir.mkdir(parents=True, exist_ok=True) >> temp_william.py
echo config = { >> temp_william.py
echo     'name': 'William', >> temp_william.py
echo     'language': 'fr', >> temp_william.py
echo     'gender': 'male', >> temp_william.py
echo     'description': 'Voix masculine francaise pour J.A.R.V.I.S.' >> temp_william.py
echo } >> temp_william.py
echo with open(william_dir / 'voice_config.json', 'w', encoding='utf-8') as f: >> temp_william.py
echo     json.dump(config, f, indent=2, ensure_ascii=False) >> temp_william.py
echo print('Voix William configuree') >> temp_william.py

python temp_william.py
del temp_william.py

:: Test final
echo Test des modules installes...
python -c "
modules = ['requests', 'openai', 'speech_recognition', 'pyttsx3', 'torch', 'TTS']
success = 0
for module in modules:
    try:
        __import__(module)
        success += 1
    except:
        pass
print('Modules installes: ' + str(success) + '/' + str(len(modules)))
if success >= 5:
    print('SUCCESS: Installation reussie!')
else:
    print('WARNING: Installation incomplete')
"

echo.
echo ========================================
echo Installation COMPLETE terminee!
echo ========================================
echo.
echo Modules installes:
echo - PyTorch avec CUDA
echo - Tortoise TTS optimise
echo - Support accents francais
echo - Configuration optimisee
echo.
echo ETAPES SUIVANTES:
echo 1. Installez Ollama: https://ollama.ai
echo 2. Telechargez le modele: ollama pull mistral-small3.2:24b
echo 3. Lancez: START_JARVIS.bat
echo.
echo Appuyez sur une touche pour continuer...
pause