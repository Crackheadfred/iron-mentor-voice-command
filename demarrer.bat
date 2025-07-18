@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo DEMARRAGE JARVIS
echo ========================================
echo.

:: Verifier si on est dans le bon dossier
if not exist "jarvis_main.py" (
    echo ERREUR: Lancez ce script depuis le dossier JARVIS
    pause
    exit
)

:: Verifier installation
if not exist "jarvis_env\Scripts\activate.bat" (
    echo ERREUR: JARVIS non installe
    echo Lancez INSTALL_AUTO.bat option 1 pour installer
    pause
    exit
)

echo Activation environnement virtuel...
call jarvis_env\Scripts\activate.bat

echo Verification de l'installation...
python verify_jarvis.py
if !ERRORLEVEL! NEQ 0 (
    echo.
    echo ========================================
    echo ERREURS DETECTEES DANS L'INSTALLATION
    echo ========================================
    echo Corrigez les erreurs avant de continuer
    echo Utilisez INSTALL_AUTO.bat pour reinstaller
    pause
    exit
)

echo.
echo ========================================
echo DEMARRAGE JARVIS...
echo ========================================
echo.
python jarvis_main.py

echo.
echo JARVIS s'est arrete
pause