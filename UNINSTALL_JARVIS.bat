@echo off
title Désinstallation J.A.R.V.I.S.

echo ========================================
echo   Désinstallation de J.A.R.V.I.S.
echo ========================================
echo.
echo Cette opération va supprimer:
echo - L'environnement virtuel Python
echo - Les logs (optionnel)
echo - La mémoire des conversations (optionnel)
echo - Les captures d'écran (optionnel)
echo.
echo Les fichiers de configuration et voix seront conservés.
echo.

set /p confirm="Êtes-vous sûr de vouloir désinstaller J.A.R.V.I.S.? (o/N): "
if /i not "%confirm%"=="o" (
    echo Opération annulée.
    pause
    exit /b 0
)

echo.
echo Désinstallation en cours...

:: Supprimer l'environnement virtuel
if exist "jarvis_env" (
    echo Suppression de l'environnement virtuel...
    rmdir /s /q "jarvis_env"
    echo ✓ Environnement virtuel supprimé
) else (
    echo ✓ Environnement virtuel non trouvé
)

:: Demander pour les logs
set /p delete_logs="Supprimer les logs? (o/N): "
if /i "%delete_logs%"=="o" (
    if exist "logs" (
        rmdir /s /q "logs"
        echo ✓ Logs supprimés
    )
)

:: Demander pour la mémoire
set /p delete_memory="Supprimer la mémoire des conversations? (o/N): "
if /i "%delete_memory%"=="o" (
    if exist "memory" (
        rmdir /s /q "memory"
        echo ✓ Mémoire supprimée
    )
)

:: Demander pour les captures
set /p delete_screenshots="Supprimer les captures d'écran? (o/N): "
if /i "%delete_screenshots%"=="o" (
    if exist "screenshots" (
        rmdir /s /q "screenshots"
        echo ✓ Captures d'écran supprimées
    )
)

:: Supprimer les fichiers temporaires
if exist "temp" (
    rmdir /s /q "temp"
    echo ✓ Fichiers temporaires supprimés
)

echo.
echo ========================================
echo Désinstallation terminée
echo ========================================
echo.
echo Fichiers conservés:
echo - config/ (configuration)
echo - voices/ (voix personnalisées)
echo - modules/ (code source)
echo - *.py, *.bat (scripts)
echo.
echo Pour réinstaller: exécutez INSTALL_JARVIS.bat
echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul