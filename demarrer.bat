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

echo Demarrage JARVIS...
echo.
python jarvis_main.py

echo.
echo JARVIS s'est arrete
pause