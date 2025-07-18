@echo off
title Installation SIMPLE J.A.R.V.I.S.
echo ========================================
echo    Installation SIMPLE J.A.R.V.I.S.
echo     (Compatible Python 3.13)
echo ========================================
echo.

:: Aller dans le repertoire du script
cd /d "%~dp0"

:: Activer l'environnement virtuel
if exist "jarvis_env\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call jarvis_env\Scripts\activate.bat
) else (
    echo ERREUR: Environnement virtuel non trouve
    echo Veuillez d'abord executer INSTALL_AUTO.bat
    goto :fin
)

echo.
echo Configuration de J.A.R.V.I.S. en francais...
echo.

:: Modifier la configuration pour forcer le francais
echo Mise a jour de la configuration...
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
echo     "tts_engine": "windows",
echo     "language": "fr",
echo     "prefer_french": true
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

:: Creer le dossier et la config William
if not exist "voices\william" mkdir voices\william
(
echo {
echo   "name": "William",
echo   "language": "fr",
echo   "gender": "male",
echo   "created": "2025-01-11",
echo   "description": "Voix Windows francaise pour J.A.R.V.I.S.",
echo   "tts_engine": "windows"
echo }
) > voices\william\voice_config.json

echo.
echo ========================================
echo    Configuration terminee!
echo ========================================
echo.
echo IMPORTANT:
echo - J.A.R.V.I.S. utilisera Windows TTS en francais
echo - Tortoise TTS non compatible avec Python 3.13
echo - Tout est configure pour fonctionner en francais
echo.
echo Vous pouvez maintenant lancer: START_JARVIS.bat
echo.

:fin
echo Appuyez sur une touche pour continuer...
pause >nul