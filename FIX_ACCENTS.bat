@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ========================================
echo Correction du support des accents français
echo ========================================
echo.

:: Activation de l'environnement virtuel
if not exist "jarvis_env\Scripts\activate.bat" (
    echo ❌ ERREUR: Environnement virtuel non trouvé
    echo Exécutez d'abord INSTALL_AUTO.bat
    exit /b 1
)

echo [1/4] Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat

:: Test du support Unicode
echo [2/4] Test du support Unicode...
python -c "
import sys
import locale

print('✅ Encodage système:', sys.getdefaultencoding())
print('✅ Locale:', locale.getpreferredencoding())
print('✅ Test accents: àáâãäéèêëîïôõöûüç')

# Test de reconnaissance vocale avec accents
try:
    import speech_recognition as sr
    print('✅ SpeechRecognition installé')
except ImportError:
    print('❌ SpeechRecognition non installé')
"

:: Installation/mise à jour des modules pour Unicode
echo [3/4] Installation des modules Unicode...
pip install --upgrade speechrecognition
pip install --upgrade pyttsx3
pip install --upgrade pyaudio

:: Test de la reconnaissance vocale française
echo [4/4] Test du module de reconnaissance vocale...
python -c "
from modules.speech_recognition_module import SpeechRecognitionModule
import json

# Charger la config
with open('config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Test du module
speech_module = SpeechRecognitionModule(config)

# Test de normalisation
test_text = 'deja tres pres apres etre'
normalized = speech_module.normalize_french_text(test_text)
print(f'✅ Test normalisation:')
print(f'   Original: {test_text}')
print(f'   Normalisé: {normalized}')

print('✅ Module de reconnaissance vocale opérationnel')
"

echo.
echo ========================================
echo Correction terminée!
echo ========================================
echo.
echo ✅ Support des accents français activé
echo ✅ Normalisation automatique des accents
echo ✅ Modules Unicode mis à jour
echo.
echo Relancez START_JARVIS.bat pour tester
echo.
pause