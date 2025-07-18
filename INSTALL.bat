@echo off
chcp 65001 > nul
echo ========================================
echo    Installation J.A.R.V.I.S. Ultimate
echo ========================================
echo.
echo Assistant Vocal Intelligent pour SimHub, DCS et Plus
echo.

:: Vérifier si on est dans le bon dossier
if not exist "jarvis_main.py" (
    echo ERREUR: Lancez ce script depuis le dossier J.A.R.V.I.S.
    pause
    exit /b 1
)

:: Nettoyer l'installation précédente
if exist "jarvis_env" (
    echo Suppression de l'ancienne installation...
    rmdir /s /q jarvis_env
)

:: Vérifier Python
echo Vérification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERREUR: Python non trouvé
    echo.
    echo Installez Python 3.8+ depuis: https://python.org
    echo IMPORTANT: Cochez "Add Python to PATH" lors de l'installation
    echo.
    pause
    exit /b 1
)

python -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)" 2>nul
if errorlevel 1 (
    echo.
    echo ❌ ERREUR: Python 3.8+ requis
    echo Votre version est trop ancienne
    echo.
    pause
    exit /b 1
)

echo ✅ Python détecté et compatible
echo.

:: Créer l'environnement virtuel
echo 📦 Création de l'environnement virtuel...
python -m venv jarvis_env
if errorlevel 1 (
    echo ❌ Erreur lors de la création de l'environnement virtuel
    pause
    exit /b 1
)

:: Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)

:: Mise à jour de pip
echo 🆙 Mise à jour de pip...
python -m pip install --upgrade pip --quiet
pip cache purge --quiet

echo.
echo ========================================
echo    Installation des dépendances
echo ========================================
echo.

:: Installation étape par étape avec vérification
echo 🔹 Installation des modules de base...
pip install requests>=2.31.0 --quiet
pip install openai>=1.40.0 --quiet
pip install psutil>=5.9.0 --quiet
echo ✅ Modules de base installés

echo.
echo 🔹 Installation des modules audio...
pip install pyttsx3>=2.90 --quiet
pip install SpeechRecognition>=3.10.0 --quiet
echo ✅ Modules audio installés

echo.
echo 🔹 Installation de NumPy (optimisé)...
pip install --only-binary=all "numpy>=1.21.0,<2.0.0" --quiet
if errorlevel 1 (
    echo ⚠️  Installation alternative de NumPy...
    pip install numpy==1.24.3 --quiet
)
echo ✅ NumPy installé

echo.
echo 🔹 Installation des modules vision...
pip install pytesseract>=0.3.10 --quiet
pip install Pillow>=10.0.0 --quiet
pip install pyautogui>=0.9.54 --quiet
echo ✅ Modules vision installés

echo.
echo 🔹 Installation d'OpenCV...
pip install opencv-python>=4.9.0 --quiet
if errorlevel 1 (
    echo ⚠️  OpenCV: installation alternative...
    pip install opencv-python-headless>=4.9.0 --quiet
)
echo ✅ OpenCV installé

echo.
echo 🔹 Installation des modules optionnels...
pip install pygame>=2.5.0 --quiet >nul 2>&1
pip install pyaudio>=0.2.14 --quiet >nul 2>&1
pip install torch>=2.0.0 --quiet >nul 2>&1
pip install scipy>=1.9.0 --quiet >nul 2>&1
echo ✅ Modules optionnels traités

:: Créer les dossiers nécessaires
echo.
echo 📁 Création des dossiers...
if not exist "logs" mkdir logs
if not exist "memory" mkdir memory
if not exist "screenshots" mkdir screenshots
if not exist "config" mkdir config
if not exist "voices\william" mkdir voices\william
if not exist "logs\telemetry" mkdir logs\telemetry
echo ✅ Dossiers créés

:: Créer le fichier de configuration par défaut
echo.
echo ⚙️  Création de la configuration...
if not exist "config\config.json" (
    echo {> config\config.json
    echo   "ollama": {>> config\config.json
    echo     "model": "mistral-small3.2:24b",>> config\config.json
    echo     "url": "http://localhost:11434">> config\config.json
    echo   },>> config\config.json
    echo   "openai": {>> config\config.json
    echo     "api_key": "",>> config\config.json
    echo     "model": "gpt-4">> config\config.json
    echo   },>> config\config.json
    echo   "voice": {>> config\config.json
    echo     "william_voice_path": "voices/william/",>> config\config.json
    echo     "tts_engine": "tortoise">> config\config.json
    echo   },>> config\config.json
    echo   "screen": {>> config\config.json
    echo     "ocr_enabled": true,>> config\config.json
    echo     "monitoring_interval": 2>> config\config.json
    echo   },>> config\config.json
    echo   "simhub": {>> config\config.json
    echo     "enabled": true,>> config\config.json
    echo     "port": 8888>> config\config.json
    echo   },>> config\config.json
    echo   "dcs": {>> config\config.json
    echo     "enabled": true,>> config\config.json
    echo     "aircraft": "F/A-18C">> config\config.json
    echo   }>> config\config.json
    echo }>> config\config.json
)
echo ✅ Configuration créée

echo.
echo ========================================
echo        Test des installations
echo ========================================
echo.

:: Test des modules installés
python -c "
import sys
print('🐍 Python:', sys.version.split()[0])
print('📍 Environnement:', sys.executable)
print()

modules = [
    ('requests', 'Requêtes HTTP'),
    ('openai', 'Client OpenAI'),
    ('speech_recognition', 'Reconnaissance vocale'),
    ('pyttsx3', 'Synthèse vocale'),
    ('psutil', 'Utilitaires système'),
    ('pytesseract', 'OCR Tesseract'),
    ('PIL', 'Traitement d\'images'),
    ('cv2', 'Vision OpenCV'),
    ('numpy', 'Calculs NumPy'),
    ('pygame', 'Audio Pygame'),
    ('pyaudio', 'Audio PyAudio')
]

success = 0
total = len(modules)

for module, desc in modules:
    try:
        __import__(module)
        print(f'✅ {desc}')
        success += 1
    except ImportError:
        print(f'⚠️  {desc} (optionnel)')

print(f'\n📊 Score: {success}/{total} modules installés')
if success >= 8:
    print('🎉 Installation RÉUSSIE!')
else:
    print('⚠️  Installation partielle - fonctionnalités limitées')
"

echo.
echo ========================================
echo       Vérifications externes
echo ========================================
echo.

:: Vérifier Ollama
echo 🤖 Vérification d'Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama non démarré ou non installé
    echo    Téléchargez: https://ollama.ai
    echo    Commandes: ollama serve
    echo              ollama pull mistral-small3.2:24b
) else (
    echo ✅ Ollama détecté et actif
)

echo.
echo 👁️  Vérification de Tesseract...
where tesseract >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Tesseract OCR non trouvé
    echo    Installez depuis: https://github.com/UB-Mannheim/tesseract/wiki
    echo    Dossier recommandé: C:\Program Files\Tesseract-OCR\
) else (
    echo ✅ Tesseract OCR détecté
)

echo.
echo ========================================
echo      Installation terminée!
echo ========================================
echo.
echo 🚀 Prochaines étapes:
echo.
echo 1. 📥 Si Ollama manque:
echo    - Téléchargez: https://ollama.ai
echo    - ollama serve
echo    - ollama pull mistral-small3.2:24b
echo.
echo 2. 👁️  Si Tesseract manque:
echo    - https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo 3. 🔑 (Optionnel) Ajoutez votre clé OpenAI:
echo    - Éditez: config\config.json
echo.
echo 4. 🎮 Pour SimHub:
echo    - Démarrez SimHub avant J.A.R.V.I.S.
echo.
echo 5. ✈️  Pour DCS:
echo    - Démarrez DCS World F/A-18C
echo.
echo 🎯 LANCEMENT:
echo    Double-cliquez sur START_JARVIS.bat
echo.
echo 🔧 DIAGNOSTIC:
echo    Lancez DIAGNOSTIC_JARVIS.bat en cas de problème
echo.
pause