@echo off
title Diagnostic Python pour J.A.R.V.I.S.
echo ========================================
echo    Diagnostic Python - J.A.R.V.I.S.
echo ========================================
echo.

echo Test des commandes Python disponibles...
echo.

:: Test python
echo [1/4] Test: python --version
python --version 2>nul
if errorlevel 1 (
    echo ❌ 'python' non trouvé
) else (
    echo ✅ 'python' fonctionne
    set PYTHON_CMD=python
    goto :found
)

:: Test python3
echo [2/4] Test: python3 --version
python3 --version 2>nul
if errorlevel 1 (
    echo ❌ 'python3' non trouvé
) else (
    echo ✅ 'python3' fonctionne
    set PYTHON_CMD=python3
    goto :found
)

:: Test py
echo [3/4] Test: py --version
py --version 2>nul
if errorlevel 1 (
    echo ❌ 'py' non trouvé
) else (
    echo ✅ 'py' fonctionne (Lanceur Python)
    set PYTHON_CMD=py
    goto :found
)

:: Test dans des chemins communs
echo [4/4] Recherche dans les dossiers standard...
set COMMON_PATHS=C:\Python39\python.exe;C:\Python310\python.exe;C:\Python311\python.exe;C:\Python312\python.exe;C:\Python313\python.exe

for %%p in (%COMMON_PATHS%) do (
    if exist "%%p" (
        echo ✅ Python trouvé: %%p
        set PYTHON_CMD="%%p"
        goto :found
    )
)

:: Aucun Python trouvé
echo.
echo ❌ AUCUN PYTHON DÉTECTÉ
echo.
echo Solutions:
echo 1. Réinstallez Python depuis python.org
echo 2. Cochez "Add to PATH" lors de l'installation
echo 3. Ou utilisez le Microsoft Store pour installer Python
echo.
goto :end

:found
echo.
echo ========================================
echo    Python détecté: %PYTHON_CMD%
echo ========================================
echo.

%PYTHON_CMD% --version
echo.

echo Test pip...
%PYTHON_CMD% -m pip --version
if errorlevel 1 (
    echo ❌ pip non trouvé
    echo Installez pip: %PYTHON_CMD% -m ensurepip --upgrade
) else (
    echo ✅ pip fonctionne
)

echo.
echo ========================================
echo    Correction du script d'installation
echo ========================================
echo.

echo Création d'un script corrigé...

:: Créer INSTALL_JARVIS_FIXED.bat
(
echo @echo off
echo title Installation J.A.R.V.I.S. - Version corrigée
echo echo Installation J.A.R.V.I.S. avec Python: %PYTHON_CMD%
echo echo.
echo.
echo :: Vérifier Python
echo %PYTHON_CMD% --version
echo if errorlevel 1 ^(
echo     echo ERREUR: Python non accessible
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo Python OK - Création environnement virtuel...
echo %PYTHON_CMD% -m venv jarvis_env
echo.
echo echo Activation environnement virtuel...
echo call jarvis_env\Scripts\activate.bat
echo.
echo echo Installation des dépendances...
echo python -m pip install --upgrade pip
echo pip install -r requirements.txt
echo.
echo echo Installation terminée!
echo echo Lancez maintenant: START_JARVIS.bat
echo pause
) > INSTALL_JARVIS_FIXED.bat

echo ✅ Script corrigé créé: INSTALL_JARVIS_FIXED.bat
echo.
echo 🚀 LANCEZ MAINTENANT: INSTALL_JARVIS_FIXED.bat
echo.

:end
echo Appuyez sur une touche pour fermer...
pause >nul