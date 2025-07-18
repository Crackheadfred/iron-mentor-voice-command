@echo off
chcp 65001 > nul
echo ========================================
echo Installation de J.A.R.V.I.S.
echo ========================================
echo.

:: Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://python.org
    echo.
    pause
    exit /b 1
)

echo Python détecté...

:: Créer un environnement virtuel
echo Création de l'environnement virtuel...
python -m venv jarvis_env
if errorlevel 1 (
    echo ERREUR: Impossible de créer l'environnement virtuel
    echo Vérifiez que vous avez les permissions d'écriture dans ce dossier
    echo.
    pause
    exit /b 1
)

:: Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat
if errorlevel 1 (
    echo ERREUR: Impossible d'activer l'environnement virtuel
    echo.
    pause
    exit /b 1
)

:: Mettre à jour pip et nettoyer le cache
echo Mise à jour de pip...
python -m pip install --upgrade pip
echo Nettoyage du cache pip pour éviter les erreurs de permission...
pip cache purge

:: Installation des dépendances principales
echo Installation des dépendances principales...
pip install requests>=2.31.0
pip install openai>=1.40.0
echo.

:: Installation de NumPy avec version compatible
echo Installation de NumPy (version compatible)...
pip install --only-binary=all "numpy>=1.21.0,<2.0.0" || pip install numpy==1.24.3
echo.

:: Installation des dépendances audio avec gestion d'erreurs
echo Installation des dépendances audio...
pip install SpeechRecognition>=3.10.0
pip install pyttsx3>=2.90
pip install psutil>=5.9.0
echo.
echo Tentative d'installation de PyAudio (peut échouer)...
pip install pyaudio || echo ATTENTION: PyAudio a echoue - installez Microsoft Visual C++ Build Tools
echo.
echo Tentative d'installation de pygame...
pip install pygame || echo ATTENTION: pygame a echoue - fonctionnalites audio limitees
echo.

:: Installation des dépendances OCR et vision avec gestion d'erreurs
echo Installation des dépendances OCR...
pip install pytesseract>=0.3.10
pip install pyautogui>=0.9.54
echo.
echo Tentative d'installation d'OpenCV...
pip install opencv-python>=4.9.0 || echo ATTENTION: OpenCV a echoue - vision limitee
echo.
echo Tentative d'installation de Pillow...
pip install Pillow>=10.0.0 || echo ATTENTION: Pillow a echoue - traitement d'images limite
echo.

:: Installation des dépendances IA avec versions compatibles
echo Installation des dépendances IA...
echo Tentative d'installation de PyTorch...
pip install torch>=2.0.0 torchaudio>=2.0.0 || echo ATTENTION: PyTorch a echoue - IA limitee
echo.
echo Tentative d'installation de Tortoise TTS...
pip install tortoise-tts>=3.0.0 || echo ATTENTION: Tortoise TTS a echoue - synthese vocale limitee
echo.

:: Installation de SciPy avec gestion d'erreurs
echo Installation de SciPy...
pip install scipy>=1.9.0 || echo ATTENTION: SciPy a echoue - installez Microsoft Visual C++ Build Tools

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
if errorlevel 1 (
    echo.
    echo ERREUR: Des problèmes ont été détectés lors du test des modules
    echo Consultez les messages ci-dessus pour plus d'informations
    echo.
    pause
)

:: Nettoyer
del test_installation.py

echo.
echo ========================================
echo Installation terminée!
echo ========================================
echo.
echo Prochaines étapes:
echo 1. Si certains modules ont échoué, installez Microsoft Visual C++ Build Tools:
echo    https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo 2. Installez Tesseract OCR (lien affiché ci-dessus)
echo 3. Démarrez Ollama et installez le modèle:
echo    ollama serve
echo    ollama pull mistral-small3.2:24b
echo 4. (Optionnel) Ajoutez votre clé API OpenAI dans config/config.json
echo 5. Lancez J.A.R.V.I.S. avec START_JARVIS.bat
echo.
echo Pour redémarrer l'installation: supprimez le dossier jarvis_env et relancez ce script
echo.
pause