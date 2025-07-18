@echo off
echo ========================================
echo Installation J.A.R.V.I.S. Ultimate
echo ========================================
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
    echo Suppression de l'ancienne installation...
    rmdir /s /q jarvis_env
)

:: Verifier Python
echo Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERREUR: Python non trouve
    echo Installez Python 3.8+ depuis: https://python.org
    echo IMPORTANT: Cochez "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo Python detecte
echo.

:: Creer l'environnement virtuel
echo Creation de l'environnement virtuel...
python -m venv jarvis_env
if errorlevel 1 (
    echo ERREUR: Impossible de creer l'environnement virtuel
    echo Verifiez les permissions ou lancez en tant qu'administrateur
    pause
    exit /b 1
)

echo Environnement virtuel cree avec succes
echo.

:: Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat
if errorlevel 1 (
    echo ERREUR: Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)

:: Mise a jour de pip
echo Mise a jour de pip...
python -m pip install --upgrade pip
pip cache purge

echo.
echo ========================================
echo Installation des dependances
echo ========================================
echo.

:: Installation des modules de base
echo Installation des modules de base...
pip install requests
pip install openai
pip install psutil
echo Modules de base installes

echo.
echo Installation des modules audio...
pip install pyttsx3
pip install SpeechRecognition
echo Modules audio installes

echo.
echo Installation de NumPy...
pip install "numpy>=1.21.0,<2.0.0"
if errorlevel 1 (
    echo Installation alternative de NumPy...
    pip install numpy==1.24.3
)
echo NumPy installe

echo.
echo Installation des modules vision...
pip install pytesseract
pip install Pillow
pip install pyautogui
echo Modules vision installes

echo.
echo Installation d'OpenCV...
pip install opencv-python
if errorlevel 1 (
    echo Installation alternative d'OpenCV...
    pip install opencv-python-headless
)
echo OpenCV installe

echo.
echo Installation des modules optionnels...
pip install pygame >nul 2>&1
pip install pyaudio >nul 2>&1
pip install torch >nul 2>&1
pip install scipy >nul 2>&1
echo Modules optionnels traites

:: Creer les dossiers necessaires
echo.
echo Creation des dossiers...
if not exist "logs" mkdir logs
if not exist "memory" mkdir memory
if not exist "screenshots" mkdir screenshots
if not exist "config" mkdir config
if not exist "voices" mkdir voices
if not exist "voices\william" mkdir voices\william
if not exist "logs\telemetry" mkdir logs\telemetry
echo Dossiers crees

:: Creer le fichier de configuration
echo.
echo Creation de la configuration...
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
echo Configuration creee

echo.
echo ========================================
echo Test des installations
echo ========================================
echo.

:: Test des modules
python -c "
import sys
print('Python:', sys.version.split()[0])
print('Environnement:', sys.executable)
print()

modules = ['requests', 'openai', 'speech_recognition', 'pyttsx3', 'psutil', 'pytesseract', 'PIL', 'cv2', 'numpy']
success = 0

for module in modules:
    try:
        __import__(module)
        print('OK -', module)
        success += 1
    except ImportError:
        print('MANQUE -', module)

print()
print('Score:', success, '/', len(modules))
if success >= 8:
    print('Installation REUSSIE!')
else:
    print('Installation partielle')
"

echo.
echo ========================================
echo Verification des outils externes
echo ========================================
echo.

:: Verifier Ollama
echo Verification d'Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ATTENTION: Ollama non detecte
    echo Installez depuis: https://ollama.ai
    echo Commandes: ollama serve
    echo           ollama pull mistral-small3.2:24b
) else (
    echo Ollama detecte et actif
)

echo.
echo Verification de Tesseract...
where tesseract >nul 2>&1
if errorlevel 1 (
    echo ATTENTION: Tesseract OCR non trouve
    echo Installez depuis: https://github.com/UB-Mannheim/tesseract/wiki
) else (
    echo Tesseract OCR detecte
)

echo.
echo ========================================
echo Installation terminee!
echo ========================================
echo.
echo Prochaines etapes:
echo.
echo 1. Si Ollama manque:
echo    - Telecharger: https://ollama.ai
echo    - ollama serve
echo    - ollama pull mistral-small3.2:24b
echo.
echo 2. Si Tesseract manque:
echo    - https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo 3. Optionnel - Cle OpenAI:
echo    - Editez: config\config.json
echo.
echo 4. LANCEMENT:
echo    - Double-cliquez sur START_JARVIS.bat
echo.
echo 5. DIAGNOSTIC:
echo    - Lancez DIAGNOSTIC_JARVIS.bat si probleme
echo.
pause