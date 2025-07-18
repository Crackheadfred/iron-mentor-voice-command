@echo off
echo ========================================
echo Installation TorToise TTS pour William
echo ========================================
echo.

:: Activer l'environnement virtuel
call jarvis_env\Scripts\activate.bat

echo Configuration de la voix francaise Windows...
echo.
echo ATTENTION: TTS (Tortoise) non compatible avec Python 3.13
echo Utilisation de Windows TTS avec voix francaise integree
echo.

echo Creation du dossier William...
if not exist "voices\william" mkdir voices\william

echo Creation de la configuration William...
(
echo {
echo   "name": "William", 
echo   "language": "fr",
echo   "gender": "male",
echo   "created": "2025-01-11",
echo   "description": "Voix masculine française pour J.A.R.V.I.S.",
echo   "tortoise_settings": {
echo     "preset": "fast",
echo     "voice_samples": [],
echo     "language_code": "fr"
echo   }
echo }
) > voices\william\voice_config.json

echo.
echo ========================================
echo TorToise TTS installe!
echo ========================================
echo.
echo La voix William est maintenant configuree.
echo Vous pouvez lancer J.A.R.V.I.S. avec START_JARVIS.bat
echo.
pause