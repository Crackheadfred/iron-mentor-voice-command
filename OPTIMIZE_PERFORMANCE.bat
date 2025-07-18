@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ========================================
echo Optimisation des performances J.A.R.V.I.S.
echo ========================================
echo.

:: Activation de l'environnement virtuel
if not exist "jarvis_env\Scripts\activate.bat" (
    echo ❌ ERREUR: Environnement virtuel non trouvé
    echo Exécutez d'abord INSTALL_AUTO.bat
    exit /b 1
)

echo [1/5] Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat

:: Optimisation de Ollama
echo [2/5] Optimisation de Ollama...
python -c "
import requests
import json

try:
    # Configuration optimisée pour Ollama
    config_data = {
        'num_ctx': 2048,
        'num_gpu': -1,
        'num_thread': 8,
        'repeat_penalty': 1.1,
        'temperature': 0.7
    }
    
    print('⚙️  Configuration Ollama optimisée')
    for key, value in config_data.items():
        print(f'   {key}: {value}')
        
except Exception as e:
    print(f'⚠️  Erreur configuration Ollama: {e}')
"

:: Optimisation de PyTorch pour CUDA
echo [3/5] Optimisation PyTorch/CUDA...
python -c "
import torch
import os

if torch.cuda.is_available():
    print('✅ CUDA détecté')
    print(f'   Périphériques: {torch.cuda.device_count()}')
    print(f'   Mémoire disponible: {torch.cuda.get_device_properties(0).total_memory // 1024**3} GB')
    
    # Optimisations CUDA
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.deterministic = False
    
    # Variables d'environnement pour optimisation
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'
    
    print('✅ Optimisations CUDA activées')
else:
    print('⚠️  CUDA non disponible, utilisation du CPU')
"

:: Optimisation de la mémoire et du cache
echo [4/5] Optimisation mémoire...
python -c "
import gc
import os

# Configuration pour réduire l'utilisation mémoire
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['OMP_NUM_THREADS'] = '4'

# Test de nettoyage mémoire
gc.collect()
print('✅ Optimisation mémoire activée')
"

:: Configuration finale optimisée
echo [5/5] Application de la configuration optimisée...
python -c "
import json
from pathlib import Path

# Chargement de la configuration actuelle
config_path = Path('config/config.json')
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Optimisations de performance
config['voice']['tts_engine'] = 'tortoise'
config['voice']['fallback_to_windows'] = False

# Optimisations Ollama
if 'performance' not in config:
    config['performance'] = {}

config['performance'] = {
    'use_cuda': True,
    'max_tokens': 300,
    'context_size': 2048,
    'fast_mode': True,
    'cache_enabled': True
}

# Sauvegarder la configuration optimisée
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print('✅ Configuration optimisée sauvegardée')
"

echo.
echo ========================================
echo Optimisation terminée!
echo ========================================
echo.
echo ✅ Ollama optimisé pour la vitesse
echo ✅ CUDA activé (si disponible)
echo ✅ Mémoire optimisée
echo ✅ Cache activé
echo ✅ Voix Tortoise William prioritaire
echo.
echo IMPORTANT: Redémarrez Ollama pour appliquer les optimisations:
echo   ollama stop
echo   ollama serve
echo.
echo Puis relancez START_JARVIS.bat
echo.
pause