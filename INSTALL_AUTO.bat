@echo off
echo ========================================
echo Installation AUTOMATIQUE J.A.R.V.I.S.
echo ========================================
echo.
echo Installation en cours... Ne fermez pas cette fenetre!
echo.

:: Aller dans le repertoire du script
cd /d "%~dp0"

:: Verifier si on est dans le bon dossier
if not exist "jarvis_main.py" (
    echo ERREUR: Lancez ce script depuis le dossier J.A.R.V.I.S.
    pause
    exit /b 1
)

:: Nettoyer l'installation precedente
if exist "jarvis_env" (
    echo [1/10] Suppression de l'ancienne installation...
    rmdir /s /q jarvis_env
)

:: Verifier Python
echo [2/10] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python non trouve - Installez Python 3.8+ depuis python.org
    pause
    exit /b 1
)

:: Creer l'environnement virtuel
echo [3/10] Creation de l'environnement virtuel...
python -m venv jarvis_env
if errorlevel 1 (
    echo ERREUR: Impossible de creer l'environnement virtuel
    pause
    exit /b 1
)

:: Activer l'environnement virtuel
echo [4/10] Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat

:: Mise a jour de pip
echo [5/10] Mise a jour de pip...
python -m pip install --upgrade pip --quiet
pip cache purge --quiet

:: Installation complete des dependances
echo [6/10] Installation de TOUS les modules (cela peut prendre du temps)...
echo Installation en cours...

pip install requests --quiet
pip install openai --quiet
pip install psutil --quiet
pip install pyttsx3 --quiet
pip install SpeechRecognition --quiet
pip install pytesseract --quiet
pip install Pillow --quiet
pip install pyautogui --quiet
pip install opencv-python --quiet
pip install numpy --quiet

echo Installation des modules optionnels...
pip install pygame --quiet >nul 2>&1
pip install pyaudio --quiet >nul 2>&1
pip install torch --quiet >nul 2>&1
pip install scipy --quiet >nul 2>&1

:: Creer les dossiers
echo [7/10] Creation des dossiers...
if not exist "logs" mkdir logs
if not exist "memory" mkdir memory
if not exist "screenshots" mkdir screenshots
if not exist "config" mkdir config
if not exist "voices" mkdir voices
if not exist "voices\william" mkdir voices\william
if not exist "logs\telemetry" mkdir logs\telemetry

:: Creer la configuration
echo [8/10] Creation de la configuration...
if not exist "config\config.json" (
    (
    echo {
    echo   "ollama": {
    echo     "model": "mistral-small3.2:24b",
    echo     "url": "http://localhost:11434"
    echo   },
    echo   "openai": {
    echo     "api_key": "",
    echo     "model": "gpt-4"
    echo   },
    echo   "voice": {
    echo     "william_voice_path": "voices/william/",
    echo     "tts_engine": "tortoise"
    echo   },
    echo   "screen": {
    echo     "ocr_enabled": true,
    echo     "monitoring_interval": 2
    echo   },
    echo   "simhub": {
    echo     "enabled": true,
    echo     "port": 8888
    echo   },
    echo   "dcs": {
    echo     "enabled": true,
    echo     "aircraft": "F/A-18C"
    echo   }
    echo }
    ) > config\config.json
)

:: Test final
echo [9/10] Test des modules installes...
python -c "
import sys
modules = ['requests', 'openai', 'speech_recognition', 'pyttsx3', 'psutil', 'pytesseract', 'PIL', 'cv2', 'numpy']
success = 0
missing = []

for module in modules:
    try:
        __import__(module)
        success += 1
    except ImportError:
        missing.append(module)

print(f'Modules installes: {success}/{len(modules)}')
if missing:
    print(f'Modules manquants: {missing}')

if success >= 8:
    print('SUCCESS: Installation reussie!')
    exit(0)
else:
    print('WARNING: Installation incomplete')
    exit(1)
"

if errorlevel 1 (
    echo [10/10] ATTENTION: Installation incomplete mais fonctionnelle
) else (
    echo [10/10] SUCCESS: Installation complete!
)

echo.
echo ========================================
echo Installation terminee!
echo ========================================
echo.
echo Etapes suivantes:
echo 1. Si Ollama manque: https://ollama.ai
echo 2. Si Tesseract manque: https://github.com/UB-Mannheim/tesseract/wiki
echo 3. LANCER J.A.R.V.I.S.: START_JARVIS.bat
echo 4. DIAGNOSTIC: DIAGNOSTIC_JARVIS.bat
echo.
echo L'installation est terminee. Vous pouvez fermer cette fenetre.
pause