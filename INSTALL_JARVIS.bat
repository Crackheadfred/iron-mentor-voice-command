@echo off
echo ========================================
echo Installation de J.A.R.V.I.S.
echo ========================================
echo.

:: Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)

echo Python détecté...

:: Créer un environnement virtuel
echo Création de l'environnement virtuel...
python -m venv jarvis_env

:: Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat

:: Mettre à jour pip
echo Mise à jour de pip...
python -m pip install --upgrade pip

:: Installation des dépendances principales
echo Installation des dépendances principales...
pip install requests==2.31.0
pip install openai==1.3.0
pip install speech-recognition==3.10.0
pip install pyttsx3==2.90
pip install pygame==2.5.2
pip install pyaudio==0.2.11
pip install psutil==5.9.6

:: Installation des dépendances OCR et vision
echo Installation des dépendances OCR...
pip install opencv-python==4.8.1.78
pip install pytesseract==0.3.10
pip install Pillow==10.1.0
pip install pyautogui==0.9.54

:: Installation de Tortoise TTS
echo Installation de Tortoise TTS...
pip install tortoise-tts==2.8.0
pip install torch==2.1.0+cu121 -f https://download.pytorch.org/whl/cu121/torch_stable.html
pip install torchaudio==2.1.0+cu121 -f https://download.pytorch.org/whl/cu121/torch_stable.html

:: Installation des dépendances NumPy et SciPy
echo Installation de NumPy et SciPy...
pip install numpy==1.24.4
pip install scipy==1.11.4

:: Créer les répertoires nécessaires
echo Création des répertoires...
if not exist "logs" mkdir logs
if not exist "memory" mkdir memory
if not exist "screenshots" mkdir screenshots
if not exist "voices\william" mkdir voices\william
if not exist "logs\telemetry" mkdir logs\telemetry

:: Télécharger et installer Tesseract (Windows)
echo.
echo ========================================
echo Installation de Tesseract OCR
echo ========================================
echo.
echo Téléchargement de Tesseract...

:: Créer un dossier temporaire
if not exist "temp" mkdir temp

:: Télécharger Tesseract (vous devrez peut-être le faire manuellement)
echo IMPORTANT: Installez manuellement Tesseract OCR depuis:
echo https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo Installez-le dans: C:\Program Files\Tesseract-OCR\
echo.

:: Vérifier Ollama
echo ========================================
echo Vérification d'Ollama
echo ========================================
echo.
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ATTENTION: Ollama ne semble pas être en cours d'exécution
    echo Assurez-vous qu'Ollama est installé et démarré
    echo Et que le modèle mistral-small3.2:24b est installé
    echo.
    echo Commandes Ollama:
    echo   ollama serve
    echo   ollama pull mistral-small3.2:24b
    echo.
) else (
    echo Ollama détecté et en cours d'exécution
)

:: Configuration finale
echo ========================================
echo Configuration finale
echo ========================================
echo.

:: Créer un script de test
echo import sys > test_installation.py
echo import importlib >> test_installation.py
echo. >> test_installation.py
echo modules = ['speech_recognition', 'pyttsx3', 'pygame', 'cv2', 'pytesseract', 'PIL', 'requests', 'openai', 'psutil'] >> test_installation.py
echo. >> test_installation.py
echo for module in modules: >> test_installation.py
echo     try: >> test_installation.py
echo         importlib.import_module(module) >> test_installation.py
echo         print(f"✓ {module}") >> test_installation.py
echo     except ImportError: >> test_installation.py
echo         print(f"✗ {module} - MANQUANT") >> test_installation.py

echo Test des modules installés...
python test_installation.py

:: Nettoyer
del test_installation.py

echo.
echo ========================================
echo Installation terminée!
echo ========================================
echo.
echo Prochaines étapes:
echo 1. Installez Tesseract OCR (lien affiché ci-dessus)
echo 2. Démarrez Ollama et installez le modèle:
echo    ollama serve
echo    ollama pull mistral-small3.2:24b
echo 3. (Optionnel) Ajoutez votre clé API OpenAI dans config/config.json
echo 4. Lancez J.A.R.V.I.S. avec START_JARVIS.bat
echo.
echo Pour redémarrer l'installation: supprimez le dossier jarvis_env et relancez ce script
echo.
pause