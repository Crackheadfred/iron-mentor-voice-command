@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ========================================
echo INSTALLATION COMPLETE J.A.R.V.I.S.
echo ========================================
echo.
echo Installation, configuration et demarrage tout-en-un
echo Ne fermez pas cette fenetre!
echo.

:: Aller dans le repertoire du script
cd /d "%~dp0"

:: Verifier si on est dans le bon dossier
if not exist "jarvis_main.py" (
    echo ERREUR: Lancez ce script depuis le dossier J.A.R.V.I.S.
    exit /b 1
)

:: Menu principal
:menu
cls
echo ========================================
echo      J.A.R.V.I.S. - MENU PRINCIPAL
echo ========================================
echo.
echo 1. INSTALLATION COMPLETE (premiere fois)
echo 2. DEMARRER J.A.R.V.I.S.
echo 3. DIAGNOSTIC ET TESTS
echo 4. MISE A JOUR
echo 5. REPARATION
echo 6. DESINSTALLATION
echo 7. QUITTER
echo.
set /p choice="Votre choix (1-7): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto start
if "%choice%"=="3" goto diagnostic
if "%choice%"=="4" goto update
if "%choice%"=="5" goto repair
if "%choice%"=="6" goto uninstall
if "%choice%"=="7" goto end
goto menu

:install
cls
echo ========================================
echo INSTALLATION COMPLETE
echo ========================================
echo.

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
    pause
    goto menu
)

:: Creer l'environnement virtuel
echo [3/12] Creation de l'environnement virtuel...
python -m venv jarvis_env
if errorlevel 1 (
    echo ERREUR: Impossible de creer l'environnement virtuel
    pause
    goto menu
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
pip install pytesseract Pillow pyautogui opencv-python numpy --quiet || echo OpenCV optionnel - peut echouer  
pip install scipy pathlib2 python-dateutil --quiet || echo Modules optionnels - peuvent echouer

:: Installation Tortoise TTS (avec gestion d'erreur)
echo [8/12] Installation Tortoise TTS...
pip install TTS --quiet
pip install tortoise-tts --quiet || echo TTS optionnel - peut echouer
pip install accelerate transformers --quiet
pip install soundfile librosa pydub --quiet || echo Audio optionnel - peut echouer

:: Installation modules audio
echo [9/12] Installation des modules audio...
pip install pygame --quiet || echo Pygame optionnel - peut echouer
pip install pyaudio --quiet || echo PyAudio optionnel - peut echouer

:: Note: sqlite3, queue, threading sont des modules integres Python

:: Creer les dossiers
echo [10/12] Creation des dossiers...
if not exist "logs" mkdir logs
if not exist "memory" mkdir memory
if not exist "screenshots" mkdir screenshots
if not exist "config" mkdir config
if not exist "voices" mkdir voices
if not exist "voices\william" mkdir voices\william
if not exist "logs\telemetry" mkdir logs\telemetry

:: Configuration
echo [11/12] Creation de la configuration...
echo import json > temp_config.py
echo config = { >> temp_config.py
echo     'ollama': { >> temp_config.py
echo         'model': 'mistral-small3.2:24b', >> temp_config.py
echo         'url': 'http://localhost:11434' >> temp_config.py
echo     }, >> temp_config.py
echo     'openai': { >> temp_config.py
echo         'api_key': '', >> temp_config.py
echo         'model': 'gpt-4.1-2025-04-14' >> temp_config.py
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
echo print('Configuration creee avec succes') >> temp_config.py

python temp_config.py
del temp_config.py

:: Configuration William
echo [12/12] Configuration de la voix William...
echo import json > temp_william.py
echo from pathlib import Path >> temp_william.py
echo william_dir = Path('voices/william') >> temp_william.py
echo config = { >> temp_william.py
echo     'name': 'William', >> temp_william.py
echo     'language': 'fr', >> temp_william.py
echo     'gender': 'male', >> temp_william.py
echo     'description': 'Voix masculine francaise pour J.A.R.V.I.S.' >> temp_william.py
echo } >> temp_william.py
echo with open(william_dir / 'voice_config.json', 'w', encoding='utf-8') as f: >> temp_william.py
echo     json.dump(config, f, indent=2, ensure_ascii=False) >> temp_william.py
echo print('Voix William configuree avec succes') >> temp_william.py

python temp_william.py
del temp_william.py

:: Test final complet de l'installation
echo Test final de l'installation...
python verify_jarvis.py
if errorlevel 1 (
    echo.
    echo ⚠️  ATTENTION: Des problemes ont ete detectes
    echo Consultez les details ci-dessus
    echo.
) else (
    echo.
    echo 🎉 INSTALLATION VALIDEE!
    echo.
)

echo.
echo ========================================
echo INSTALLATION TERMINEE!
echo ========================================
echo.
echo ETAPES SUIVANTES:
echo 1. Installez Ollama: https://ollama.ai
echo 2. Telechargez le modele: ollama pull mistral-small3.2:24b
echo.
pause
goto menu

:start
cls
echo ========================================
echo DEMARRAGE J.A.R.V.I.S.
echo ========================================
echo.

if not exist "jarvis_env\Scripts\activate.bat" (
    echo ERREUR: J.A.R.V.I.S. non installe
    echo Choisissez l'option 1 pour l'installer
    pause
    goto menu
)

echo Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat

echo Verification des services...

:: Verifier Ollama
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ATTENTION: Ollama non detecte
    echo Demarrez Ollama avant de continuer
    echo.
    set /p continue="Continuer quand meme? (o/n): "
    if not "!continue!"=="o" goto menu
)

:: Verifier Tesseract
where tesseract >nul 2>&1
if errorlevel 1 (
    echo ATTENTION: Tesseract OCR non detecte
    echo L'analyse d'ecran sera desactivee
    echo.
)

echo.
echo Demarrage de J.A.R.V.I.S...
echo.

python jarvis_main.py
goto menu

:diagnostic
cls
echo ========================================
echo DIAGNOSTIC J.A.R.V.I.S.
echo ========================================
echo.

if not exist "jarvis_env\Scripts\activate.bat" (
    echo ERREUR: J.A.R.V.I.S. non installe
    pause
    goto menu
)

call jarvis_env\Scripts\activate.bat

echo Test des modules...
python -c "
modules = ['requests', 'openai', 'speech_recognition', 'pyttsx3', 'torch', 'TTS', 'cv2', 'numpy', 'pygame', 'PIL', 'psutil', 'json', 'logging', 'pathlib']
success = 0
failed = []
for module in modules:
    try:
        if module == 'pathlib':
            from pathlib import Path
        elif module == 'cv2':
            import cv2
        elif module == 'PIL':
            from PIL import Image
        else:
            __import__(module)
        print(f'✓ {module}')
        success += 1
    except Exception as e:
        print(f'✗ {module} - {str(e)[:50]}')
        failed.append(module)
print(f'\\nResultat: {success}/{len(modules)} modules OK')
if failed:
    print(f'Modules echoues: {failed}')
"

echo.
echo Test des modules J.A.R.V.I.S...
python -c "
import sys
sys.path.append('.')
try:
    from modules.ollama_client import OllamaClient
    print('✓ OllamaClient OK')
except Exception as e:
    print(f'✗ OllamaClient: {e}')

try:
    from modules.voice_manager import VoiceManager  
    print('✓ VoiceManager OK')
except Exception as e:
    print(f'✗ VoiceManager: {e}')

try:
    from modules.speech_recognition_module import SpeechRecognitionModule
    print('✓ SpeechRecognitionModule OK')
except Exception as e:
    print(f'✗ SpeechRecognitionModule: {e}')

try:
    from modules.screen_monitor import ScreenMonitor
    print('✓ ScreenMonitor OK')
except Exception as e:
    print(f'✗ ScreenMonitor: {e}')

try:
    from modules.memory_manager import MemoryManager
    print('✓ MemoryManager OK')
except Exception as e:
    print(f'✗ MemoryManager: {e}')
"

echo.
echo Test Ollama...
curl -s http://localhost:11434/api/tags && echo ✓ Ollama OK || echo ✗ Ollama KO

echo.
echo Test microphone...
python -c "
import speech_recognition as sr
try:
    r = sr.Recognizer()
    m = sr.Microphone()
    print('✓ Microphone detecte')
except:
    print('✗ Probleme microphone')
"

pause
goto menu

:update
cls
echo ========================================
echo MISE A JOUR J.A.R.V.I.S.
echo ========================================
echo.

if not exist "jarvis_env\Scripts\activate.bat" (
    echo ERREUR: J.A.R.V.I.S. non installe
    pause
    goto menu
)

call jarvis_env\Scripts\activate.bat

echo Mise a jour des modules...
pip install --upgrade torch TTS tortoise-tts requests openai numpy opencv-python
pip install --upgrade SpeechRecognition pyttsx3 pygame pyaudio
echo Mise a jour terminee!
pause
goto menu

:repair
cls
echo ========================================
echo REPARATION J.A.R.V.I.S.
echo ========================================
echo.

if not exist "jarvis_env\Scripts\activate.bat" (
    echo ERREUR: J.A.R.V.I.S. non installe
    pause
    goto menu
)

call jarvis_env\Scripts\activate.bat

echo Reinstallation des modules problematiques...
pip install --force-reinstall pyaudio pygame pyttsx3 SpeechRecognition
pip install --force-reinstall opencv-python pytesseract Pillow numpy

echo Reconfiguration de la voix...
python -c "
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if 'fr' in voice.id.lower() or 'french' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        print(f'Voix francaise configuree: {voice.name}')
        break
engine.stop()
"

echo Reparation terminee!
pause
goto menu

:uninstall
cls
echo ========================================
echo DESINSTALLATION J.A.R.V.I.S.
echo ========================================
echo.
echo ATTENTION: Ceci supprimera completement J.A.R.V.I.S.
echo.
set /p confirm="Confirmer la desinstallation? (oui/non): "
if not "%confirm%"=="oui" goto menu

echo Suppression en cours...
if exist "jarvis_env" rmdir /s /q jarvis_env
if exist "logs" rmdir /s /q logs
if exist "memory" rmdir /s /q memory
if exist "screenshots" rmdir /s /q screenshots
if exist "voices" rmdir /s /q voices

echo Desinstallation terminee!
pause
goto menu

:end
echo Au revoir!
pause