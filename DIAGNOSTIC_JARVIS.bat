@echo off
title J.A.R.V.I.S. - Diagnostic

echo ========================================
echo   J.A.R.V.I.S. - Diagnostic Système
echo ========================================
echo.

:: Vérifier si l'environnement virtuel existe
if exist "jarvis_env\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call jarvis_env\Scripts\activate.bat
    echo.
) else (
    echo ATTENTION: Environnement virtuel non trouvé
    echo Utilisation de l'environnement Python global
    echo.
)

:: Lancer le diagnostic
echo Lancement du diagnostic...
echo.
python setup_dev.py

echo.
echo ========================================
echo Diagnostic terminé
echo ========================================
echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul