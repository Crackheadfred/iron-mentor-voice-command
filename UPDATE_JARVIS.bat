@echo off
title Mise à jour J.A.R.V.I.S.

echo ========================================
echo   Mise à jour de J.A.R.V.I.S.
echo ========================================
echo.

:: Vérifier si l'environnement virtuel existe
if not exist "jarvis_env\Scripts\activate.bat" (
    echo ERREUR: Environnement virtuel non trouvé
    echo Veuillez d'abord exécuter INSTALL_JARVIS.bat
    pause
    exit /b 1
)

:: Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat

echo.
echo ========================================
echo Mise à jour des dépendances
echo ========================================
echo.

:: Mettre à jour pip
echo Mise à jour de pip...
python -m pip install --upgrade pip

:: Mettre à jour les dépendances principales
echo Mise à jour des dépendances...
pip install --upgrade requests openai speech-recognition pyttsx3 pygame
pip install --upgrade opencv-python pytesseract Pillow pyautogui psutil
pip install --upgrade numpy scipy

:: Mettre à jour PyTorch si nécessaire
echo Vérification de PyTorch...
python -c "import torch; print(f'PyTorch version: {torch.__version__}')" 2>nul
if errorlevel 1 (
    echo Installation de PyTorch avec CUDA...
    pip install torch==2.1.0+cu121 torchaudio==2.1.0+cu121 -f https://download.pytorch.org/whl/cu121/torch_stable.html
)

:: Mettre à jour Tortoise TTS si disponible
echo Vérification de Tortoise TTS...
pip install --upgrade tortoise-tts 2>nul
if errorlevel 1 (
    echo Tortoise TTS non mis à jour (normal si pas installé)
)

echo.
echo ========================================
echo Vérification post-mise à jour
echo ========================================
echo.

:: Test des modules
python -c "
import sys
modules = ['speech_recognition', 'pyttsx3', 'pygame', 'cv2', 'pytesseract', 'PIL', 'requests', 'openai', 'psutil']
for module in modules:
    try:
        __import__(module)
        print(f'✓ {module}')
    except ImportError:
        print(f'✗ {module} - ERREUR')
"

echo.
echo ========================================
echo Mise à jour de la configuration
echo ========================================
echo.

:: Vérifier la configuration
if not exist "config\config.json" (
    echo Création de la configuration par défaut...
    python -c "
import json
from pathlib import Path
config = {
    'ollama': {'model': 'mistral-small3.2:24b', 'url': 'http://localhost:11434'},
    'openai': {'api_key': '', 'model': 'gpt-4'},
    'voice': {'william_voice_path': 'voices/william/', 'tts_engine': 'tortoise'},
    'screen': {'ocr_enabled': True, 'monitoring_interval': 2},
    'simhub': {'enabled': True, 'port': 8888},
    'dcs': {'enabled': True, 'aircraft': 'F/A-18C'}
}
Path('config').mkdir(exist_ok=True)
with open('config/config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print('Configuration créée')
"
) else (
    echo Configuration existante préservée
)

echo.
echo ========================================
echo Test de fonctionnement
echo ========================================
echo.

:: Test rapide
echo Test des modules J.A.R.V.I.S...
python -c "
try:
    from modules.ollama_client import OllamaClient
    from modules.memory_manager import MemoryManager
    print('✓ Modules J.A.R.V.I.S. OK')
except Exception as e:
    print(f'✗ Erreur modules: {e}')
"

:: Vérifier Ollama
echo Test de connexion Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama non connecté
    echo    Démarrez avec: ollama serve
) else (
    echo ✓ Ollama connecté
)

echo.
echo ========================================
echo Mise à jour terminée
echo ========================================
echo.
echo Changelog probable:
echo - Dépendances Python mises à jour
echo - Configuration vérifiée
echo - Modules testés
echo.
echo Si vous rencontrez des problèmes:
echo 1. Exécutez DIAGNOSTIC_JARVIS.bat
echo 2. Consultez les logs dans logs/
echo 3. Redémarrez Ollama si nécessaire
echo.
echo Pour lancer J.A.R.V.I.S.: START_JARVIS.bat
echo.
pause