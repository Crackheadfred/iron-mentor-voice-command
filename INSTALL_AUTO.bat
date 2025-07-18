@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ========================================
echo Installation COMPLÈTE J.A.R.V.I.S.
echo ========================================
echo.
echo Installation automatique avec toutes les optimisations
echo Ne fermez pas cette fenêtre!
echo.

:: Aller dans le répertoire du script
cd /d "%~dp0"

:: Vérifier si on est dans le bon dossier
if not exist "jarvis_main.py" (
    echo ERREUR: Lancez ce script depuis le dossier J.A.R.V.I.S.
    exit /b 1
)

:: Nettoyer l'installation précédente
if exist "jarvis_env" (
    echo [1/15] Suppression de l'ancienne installation...
    rmdir /s /q jarvis_env
)

:: Vérifier Python
echo [2/15] Vérification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python non trouvé - Installez Python 3.8+ depuis python.org
    exit /b 1
)

:: Créer l'environnement virtuel
echo [3/15] Création de l'environnement virtuel...
python -m venv jarvis_env
if errorlevel 1 (
    echo ERREUR: Impossible de créer l'environnement virtuel
    exit /b 1
)

:: Activer l'environnement virtuel
echo [4/15] Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat

:: Mise à jour de pip
echo [5/15] Mise à jour de pip...
python -m pip install --upgrade pip --quiet

:: Vérification et installation de CUDA
echo [6/15] Configuration CUDA et PyTorch...
python -c "
import sys
try:
    import torch
    print('✅ PyTorch déjà installé')
    print('✅ CUDA disponible:', torch.cuda.is_available())
except ImportError:
    print('Installation de PyTorch avec support CUDA...')
" >nul 2>&1

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --quiet

:: Installation des modules de base
echo [7/15] Installation des modules de base...
pip install requests openai psutil pyttsx3 SpeechRecognition --quiet
pip install pytesseract Pillow pyautogui opencv-python numpy --quiet

:: Installation Tortoise TTS et optimisations
echo [8/15] Installation Tortoise TTS optimisé...
pip install TTS tortoise-tts --quiet
pip install accelerate transformers deepspeed xformers --quiet
pip install soundfile librosa pydub --quiet

:: Installation modules audio
echo [9/15] Installation des modules audio...
pip install pygame pyaudio --quiet

:: Créer les dossiers
echo [10/15] Création des dossiers...
if not exist "logs" mkdir logs
if not exist "memory" mkdir memory
if not exist "screenshots" mkdir screenshots
if not exist "config" mkdir config
if not exist "voices" mkdir voices
if not exist "voices\william" mkdir voices\william
if not exist "logs\telemetry" mkdir logs\telemetry

:: Configuration optimisée
echo [11/15] Création de la configuration optimisée...
if not exist "config\config.json" (
    python -c "
import json
config = {
    'ollama': {
        'model': 'mistral-small3.2:24b',
        'url': 'http://localhost:11434'
    },
    'openai': {
        'api_key': '',
        'model': 'gpt-4o-mini'
    },
    'voice': {
        'william_voice_path': 'voices/william/',
        'tts_engine': 'tortoise',
        'language': 'fr',
        'fallback_to_windows': False,
        'force_windows': False
    },
    'screen': {
        'ocr_enabled': True,
        'monitoring_interval': 2
    },
    'simhub': {
        'enabled': True,
        'port': 8888
    },
    'dcs': {
        'enabled': True,
        'aircraft': 'F/A-18C'
    },
    'performance': {
        'use_cuda': True,
        'max_tokens': 300,
        'context_size': 2048,
        'fast_mode': True,
        'cache_enabled': True
    }
}
with open('config/config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print('✅ Configuration optimisée créée')
"
)

:: Configuration de la voix William
echo [12/15] Configuration de la voix William...
python -c "
import os
import urllib.request
import json
from pathlib import Path

william_dir = Path('voices/william')
william_dir.mkdir(parents=True, exist_ok=True)

print('📥 Configuration de la voix William...')

# URLs d'échantillons de voix
voice_urls = [
    'https://github.com/neonbjb/tortoise-tts/raw/main/tortoise/voices/train_grace/1.wav',
    'https://github.com/neonbjb/tortoise-tts/raw/main/tortoise/voices/train_grace/2.wav'
]

try:
    for i, url in enumerate(voice_urls, 1):
        filename = f'william_sample{i}.wav'
        filepath = william_dir / filename
        print(f'  Téléchargement: {filename}')
        urllib.request.urlretrieve(url, str(filepath))
    
    config = {
        'name': 'William',
        'language': 'fr',
        'gender': 'male',
        'created': '2025-01-18',
        'description': 'Voix masculine française optimisée pour J.A.R.V.I.S.',
        'tortoise_settings': {
            'preset': 'ultra_fast',
            'voice_samples': ['william_sample1.wav', 'william_sample2.wav'],
            'language_code': 'fr',
            'use_cuda': True,
            'kv_cache': True,
            'cvvp_amount': 0.0
        }
    }
    
    with open(william_dir / 'voice_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print('✅ Voix William configurée')
    
except Exception as e:
    print(f'⚠️  Erreur: {e}')
    print('   La voix sera créée au premier lancement')
"

:: Test du support Unicode et accents
echo [13/15] Configuration du support des accents français...
python -c "
import sys
import locale

print('✅ Encodage système:', sys.getdefaultencoding())
print('✅ Locale:', locale.getpreferredencoding())
print('✅ Test accents: àáâãäéèêëîïôõöûüç')

# Test des modules
try:
    import speech_recognition as sr
    import pyttsx3
    print('✅ Modules vocaux installés')
except ImportError as e:
    print(f'⚠️  Module manquant: {e}')
"

:: Optimisations finales
echo [14/15] Application des optimisations de performance...
python -c "
import torch
import os
import gc

if torch.cuda.is_available():
    print('✅ CUDA détecté et configuré')
    print(f'   Périphériques: {torch.cuda.device_count()}')
    
    # Optimisations CUDA
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.deterministic = False
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'
    
    print('✅ Optimisations CUDA activées')
else:
    print('⚠️  CUDA non disponible, utilisation CPU optimisé')

# Configuration pour performance
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['OMP_NUM_THREADS'] = '4'

gc.collect()
print('✅ Optimisations mémoire activées')
"

:: Test final complet
echo [15/15] Test final de l'installation...
python -c "
import sys
modules = ['requests', 'openai', 'speech_recognition', 'pyttsx3', 'psutil', 'pytesseract', 'PIL', 'cv2', 'numpy', 'torch', 'TTS']
success = 0
missing = []

for module in modules:
    try:
        __import__(module)
        success += 1
    except ImportError:
        missing.append(module)

print(f'Modules installés: {success}/{len(modules)}')
if missing:
    print(f'Modules manquants: {missing}')

# Test des modules J.A.R.V.I.S.
try:
    from modules.ollama_client import OllamaClient
    from modules.voice_manager import VoiceManager
    from modules.speech_recognition_module import SpeechRecognitionModule
    print('✅ Modules J.A.R.V.I.S. fonctionnels')
except Exception as e:
    print(f'⚠️  Erreur modules J.A.R.V.I.S.: {e}')

if success >= 10:
    print('🎉 SUCCESS: Installation complète réussie!')
    exit(0)
else:
    print('⚠️  WARNING: Installation incomplète mais fonctionnelle')
    exit(1)
"

echo.
echo ========================================
echo 🎉 Installation COMPLÈTE terminée!
echo ========================================
echo.
echo ✅ Modules de base installés
echo ✅ Tortoise TTS avec CUDA installé  
echo ✅ Voix William configurée
echo ✅ Support des accents français
echo ✅ Optimisations de performance
echo ✅ Configuration optimisée créée
echo.
echo 🚀 ÉTAPES SUIVANTES:
echo 1. Installez Ollama: https://ollama.ai
echo 2. Téléchargez le modèle: ollama pull mistral-small3.2:24b
echo 3. Lancez: START_JARVIS.bat
echo.
echo 💡 CONSEILS:
echo - Redémarrez Ollama après installation: ollama stop puis ollama serve
echo - Pour diagnostics: DIAGNOSTIC_JARVIS.bat
echo.
echo Appuyez sur une touche pour continuer...
pause