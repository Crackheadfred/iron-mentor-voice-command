@echo off
setlocal EnableDelayedExpansion

:menu
cls
echo ========================================
echo INSTALLATION JARVIS - MENU PRINCIPAL
echo ========================================
echo.
echo 1. INSTALLATION COMPLETE (premiere fois)
echo 2. DEMARRER JARVIS
echo 3. DIAGNOSTIC ET TESTS
echo 4. MISE A JOUR
echo 5. REPARATION
echo 6. DESINSTALLATION
echo 7. QUITTER
echo.

set /p choice="Votre choix (1-7): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto start
if "%choice%"=="3" goto diagnostic
if "%choice%"=="4" goto update
if "%choice%"=="5" goto repair
if "%choice%"=="6" goto uninstall
if "%choice%"=="7" goto end

echo Choix invalide.
timeout /t 2 >nul
goto menu

:install
cls
echo ========================================
echo INSTALLATION COMPLETE
echo ========================================
echo.

:: Verifier si on est dans le bon dossier
if not exist "jarvis_main.py" (
    echo ERREUR: Lancez ce script depuis le dossier JARVIS
    pause
    goto menu
)

:: Nettoyer installation precedente
if exist "jarvis_env" (
    echo [1/10] Suppression ancienne installation...
    rmdir /s /q jarvis_env
)

:: Verifier Python
echo [2/10] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python non trouve
    echo Installez Python 3.8+ depuis python.org
    pause
    goto menu
)

:: Creer environnement virtuel
echo [3/10] Creation environnement virtuel...
python -m venv jarvis_env
if errorlevel 1 (
    echo ERREUR: Impossible de creer environnement virtuel
    pause
    goto menu
)

:: Activer environnement virtuel
echo [4/10] Activation environnement virtuel...
call jarvis_env\Scripts\activate.bat

:: Mise a jour pip
echo [5/10] Mise a jour pip...
python -m pip install --upgrade pip --quiet

:: Installation PyTorch
echo [6/10] Installation PyTorch...
pip install torch torchvision torchaudio --quiet

:: Installation modules de base
echo [7/10] Installation modules de base...
pip install requests openai psutil pyttsx3 SpeechRecognition --quiet
pip install pytesseract Pillow pyautogui opencv-python numpy --quiet

:: Installation TTS (optionnel)
echo [8/10] Installation TTS (peut echouer)...
pip install TTS --quiet || echo TTS echoue - Windows TTS sera utilise
pip install accelerate transformers --quiet || echo Modules optionnels

:: Installation modules audio
echo [9/10] Installation modules audio...
pip install pygame --quiet
pip install pyaudio --quiet

:: Creer dossiers
echo [10/10] Creation dossiers...
if not exist "logs" mkdir logs
if not exist "memory" mkdir memory
if not exist "screenshots" mkdir screenshots
if not exist "config" mkdir config
if not exist "voices" mkdir voices
if not exist "voices\william" mkdir voices\william

:: Configuration
echo Creation configuration...
echo import json > temp_config.py
echo config = { >> temp_config.py
echo     "ollama": { >> temp_config.py
echo         "model": "mistral-small3.2:24b", >> temp_config.py
echo         "url": "http://localhost:11434" >> temp_config.py
echo     }, >> temp_config.py
echo     "openai": { >> temp_config.py
echo         "api_key": "", >> temp_config.py
echo         "model": "gpt-4.1-2025-04-14" >> temp_config.py
echo     }, >> temp_config.py
echo     "voice": { >> temp_config.py
echo         "william_voice_path": "voices/william/", >> temp_config.py
echo         "tts_engine": "windows", >> temp_config.py
echo         "language": "fr", >> temp_config.py
echo         "fallback_to_windows": True >> temp_config.py
echo     }, >> temp_config.py
echo     "screen": { >> temp_config.py
echo         "ocr_enabled": True, >> temp_config.py
echo         "monitoring_interval": 2 >> temp_config.py
echo     }, >> temp_config.py
echo     "simhub": { >> temp_config.py
echo         "enabled": True, >> temp_config.py
echo         "port": 8888 >> temp_config.py
echo     }, >> temp_config.py
echo     "dcs": { >> temp_config.py
echo         "enabled": True, >> temp_config.py
echo         "aircraft": "F/A-18C" >> temp_config.py
echo     } >> temp_config.py
echo } >> temp_config.py
echo with open('config/config.json', 'w', encoding='utf-8') as f: >> temp_config.py
echo     json.dump(config, f, indent=2, ensure_ascii=False) >> temp_config.py

python temp_config.py
del temp_config.py

:: Configuration William
echo import json > temp_william.py
echo from pathlib import Path >> temp_william.py
echo william_dir = Path('voices/william') >> temp_william.py
echo config = {"name": "William", "language": "fr", "gender": "male"} >> temp_william.py
echo with open(william_dir / 'voice_config.json', 'w') as f: >> temp_william.py
echo     json.dump(config, f, indent=2) >> temp_william.py

python temp_william.py
del temp_william.py

echo.
echo ========================================
echo INSTALLATION TERMINEE!
echo ========================================
echo.
echo Configuration: Windows TTS utilise (plus stable)
echo Si TTS a echoue: pas de probleme, Windows TTS fonctionne
echo.
echo ETAPES SUIVANTES:
echo 1. Installez Ollama: https://ollama.ai
echo 2. Commande: ollama pull mistral-small3.2:24b
echo 3. Lancez option 2 pour demarrer JARVIS
echo.
pause
goto menu

:start
cls
echo Demarrage JARVIS...
if not exist "jarvis_env\Scripts\activate.bat" (
    echo ERREUR: JARVIS non installe
    echo Choisissez option 1 pour installer
    pause
    goto menu
)

call jarvis_env\Scripts\activate.bat
python jarvis_main.py
goto menu

:diagnostic
cls
echo Test des modules...
if not exist "jarvis_env\Scripts\activate.bat" (
    echo ERREUR: JARVIS non installe
    pause
    goto menu
)

call jarvis_env\Scripts\activate.bat
python -c "
modules = ['requests', 'openai', 'torch', 'pyttsx3', 'speech_recognition', 'cv2', 'numpy']
success = 0
for module in modules:
    try:
        if module == 'cv2':
            import cv2
        else:
            __import__(module)
        print('OK:', module)
        success += 1
    except:
        print('MANQUANT:', module)
print('Resultat:', success, '/', len(modules), 'modules OK')
if success >= 5:
    print('JARVIS peut fonctionner!')
else:
    print('Installation incomplete')
"
pause
goto menu

:update
cls
echo Mise a jour...
if not exist "jarvis_env\Scripts\activate.bat" (
    echo ERREUR: JARVIS non installe
    pause
    goto menu
)

call jarvis_env\Scripts\activate.bat
pip install --upgrade torch requests openai pyttsx3 SpeechRecognition
pip install --upgrade numpy opencv-python
echo Mise a jour terminee
pause
goto menu

:repair
cls
echo Reparation...
if not exist "jarvis_env\Scripts\activate.bat" (
    echo ERREUR: JARVIS non installe
    pause
    goto menu
)

call jarvis_env\Scripts\activate.bat
pip install --force-reinstall pyttsx3 SpeechRecognition
echo Reparation terminee
pause
goto menu

:uninstall
cls
echo ATTENTION: Suppression complete de JARVIS
set /p confirm="Confirmer (oui/non): "
if not "%confirm%"=="oui" goto menu

if exist "jarvis_env" rmdir /s /q jarvis_env
if exist "logs" rmdir /s /q logs
if exist "memory" rmdir /s /q memory
if exist "screenshots" rmdir /s /q screenshots
if exist "voices" rmdir /s /q voices
echo Desinstallation terminee
pause
goto menu

:end
echo Au revoir!
pause
exit