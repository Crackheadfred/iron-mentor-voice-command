@echo off
echo ========================================
echo Installation TorToise TTS pour William
echo ========================================
echo.

:: Activer l'environnement virtuel
call jarvis_env\Scripts\activate.bat

echo Installation de TorToise TTS...
pip install TTS

echo Installation de modeles vocaux francais...
pip install espeak-ng

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