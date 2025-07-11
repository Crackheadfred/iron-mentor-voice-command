@echo off
title J.A.R.V.I.S. - Assistant Vocal Intelligent

echo ========================================
echo      J.A.R.V.I.S. - Démarrage
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

:: Vérifier les services requis
echo Vérification des services...

:: Vérifier Ollama
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  ATTENTION: Ollama ne répond pas
    echo    Démarrez Ollama avec: ollama serve
    echo    Puis installez le modèle: ollama pull mistral-small3.2:24b
    echo.
    set /p continue="Continuer malgré tout? (o/N): "
    if /i not "%continue%"=="o" (
        pause
        exit /b 1
    )
) else (
    echo ✓ Ollama détecté
)

:: Vérifier Tesseract
where tesseract >nul 2>&1
if errorlevel 1 (
    if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
        echo ✓ Tesseract détecté
    ) else (
        echo ⚠️  Tesseract non trouvé - OCR désactivé
    )
) else (
    echo ✓ Tesseract détecté
)

echo.
echo ========================================
echo     Démarrage de J.A.R.V.I.S.
echo ========================================
echo.
echo Commandes disponibles pendant l'exécution:
echo - Commandes vocales: parlez normalement
echo - Commandes clavier: tapez et appuyez sur Entrée
echo - Arrêt: Ctrl+C ou tapez "exit"
echo.
echo Commandes spéciales:
echo - "Silence" / "C'est beau" : mode silencieux
echo - "J.A.R.V.I.S., t'es là?" : réactivation
echo - "Utilise ChatGPT" : utiliser OpenAI
echo - "Analyse l'écran" : analyse OCR
echo - "Analyse mon tour" : conseils SimHub
echo - "Active le module F-18" : aide DCS
echo.

:: Créer un fichier de log pour cette session
set LOG_FILE=logs\jarvis_session_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
echo Session démarrée le %date% à %time% > "%LOG_FILE%"

:: Lancer J.A.R.V.I.S.
echo Lancement de J.A.R.V.I.S...
echo.
python jarvis_main.py

echo.
echo ========================================
echo    J.A.R.V.I.S. fermé
echo ========================================
echo Session terminée le %date% à %time% >> "%LOG_FILE%"
echo.
pause