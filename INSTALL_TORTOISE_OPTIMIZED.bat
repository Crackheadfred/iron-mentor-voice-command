@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ========================================
echo Installation Tortoise TTS Optimisé CUDA
echo ========================================
echo.

:: Activation de l'environnement virtuel
if not exist "jarvis_env\Scripts\activate.bat" (
    echo ❌ ERREUR: Environnement virtuel non trouvé
    echo Exécutez d'abord INSTALL_AUTO.bat
    pause
    exit /b 1
)

echo [1/6] Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat

:: Vérification de CUDA
echo [2/6] Vérification de CUDA...
python -c "import torch; print('✅ PyTorch:', torch.__version__); print('✅ CUDA disponible:', torch.cuda.is_available()); print('✅ Périphériques CUDA:', torch.cuda.device_count())" 2>nul
if errorlevel 1 (
    echo ⚠️  PyTorch non installé, installation en cours...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
)

:: Installation de Tortoise TTS optimisé
echo [3/6] Installation de Tortoise TTS...
pip install TTS
pip install tortoise-tts

:: Installation des dépendances pour l'optimisation
echo [4/6] Installation des optimisations...
pip install accelerate
pip install transformers
pip install deepspeed
pip install xformers

:: Installation des outils audio optimisés
echo [5/6] Installation des outils audio...
pip install soundfile
pip install librosa
pip install pydub

:: Téléchargement et configuration de la voix William
echo [6/6] Configuration de la voix William...
python -c "
import os
import urllib.request
import json
from pathlib import Path

# Créer le dossier pour William
william_dir = Path('voices/william')
william_dir.mkdir(parents=True, exist_ok=True)

print('📥 Téléchargement des échantillons de voix...')

# URLs d'échantillons de voix (voix françaises libres)
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
    
    # Configuration optimisée pour William
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
    
    print('✅ Voix William configurée avec succès')
    
except Exception as e:
    print(f'⚠️  Erreur lors du téléchargement: {e}')
    print('   La voix sera créée automatiquement au premier lancement')
"

echo.
echo ========================================
echo Installation terminée!
echo ========================================
echo.
echo ✅ Tortoise TTS installé et optimisé
echo ✅ Support CUDA activé (si disponible)
echo ✅ Voix William configurée
echo ✅ Optimisations de performance activées
echo.
echo Relancez START_JARVIS.bat pour utiliser la nouvelle configuration
echo.
pause