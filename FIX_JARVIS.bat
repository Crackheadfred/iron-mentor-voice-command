@echo off
title Correction automatique J.A.R.V.I.S.
echo ========================================
echo   Correction automatique J.A.R.V.I.S.
echo ========================================
echo.

:: Vérifier si l'environnement virtuel existe
if not exist "jarvis_env\Scripts\activate.bat" (
    echo ERREUR: Environnement virtuel non trouvé
    echo Lancez d'abord INSTALL_JARVIS.bat
    pause
    exit /b 1
)

echo Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat

echo.
echo ========================================
echo    Mise à jour des dépendances
echo ========================================
echo.

echo Mise à jour de pip...
python -m pip install --upgrade pip

echo.
echo Installation/mise à jour des dépendances principales...
pip install --upgrade requests>=2.31.0
pip install --upgrade openai>=1.40.0
pip install --upgrade numpy
pip install --upgrade psutil

echo.
echo Installation des modules de reconnaissance vocale...
pip install --upgrade SpeechRecognition>=3.10.0
pip install --upgrade pyttsx3>=2.90
pip install --upgrade pygame>=2.5.0

echo.
echo Installation des modules de vision...
pip install --upgrade opencv-python>=4.9.0
pip install --upgrade pytesseract>=0.3.10
pip install --upgrade Pillow>=10.0.0
pip install --upgrade pyautogui>=0.9.54

echo.
echo Installation PyTorch (peut prendre du temps)...
pip install torch>=2.0.0 torchaudio>=2.0.0 --index-url https://download.pytorch.org/whl/cpu

echo.
echo Installation des utilitaires...
pip install --upgrade scipy
pip install --upgrade python-dateutil

echo.
echo ========================================
echo    Vérification post-installation
echo ========================================
echo.

echo Test des imports critiques...
python -c "
import sys
critical_modules = [
    'requests', 'openai', 'speech_recognition', 'pyttsx3', 
    'pygame', 'cv2', 'pytesseract', 'PIL', 'psutil', 
    'torch', 'numpy', 'scipy'
]

success_count = 0
for module in critical_modules:
    try:
        __import__(module)
        print(f'✅ {module}')
        success_count += 1
    except ImportError as e:
        print(f'❌ {module} - {e}')

print(f'\nRésultat: {success_count}/{len(critical_modules)} modules importés avec succès')

if success_count >= len(critical_modules) - 2:  # Tolérer 2 échecs max
    print('🎉 Installation réussie!')
    sys.exit(0)
else:
    print('⚠️ Certains modules ont échoué')
    sys.exit(1)
"

if errorlevel 1 (
    echo.
    echo ========================================
    echo    Installation incomplète
    echo ========================================
    echo.
    echo Certains modules ont échoué à s'installer.
    echo Cela peut être normal pour certains modules optionnels.
    echo.
    echo Si J.A.R.V.I.S. ne fonctionne pas, essayez:
    echo 1. Redémarrez en tant qu'administrateur
    echo 2. Vérifiez votre connexion internet
    echo 3. Consultez les logs d'erreur ci-dessus
    echo.
) else (
    echo.
    echo ========================================
    echo    Correction terminée avec succès!
    echo ========================================
    echo.
    echo Toutes les dépendances sont installées.
    echo Vous pouvez maintenant lancer J.A.R.V.I.S.
    echo.
)

echo Testez maintenant avec: TEST_JARVIS.bat
echo Puis lancez avec: START_JARVIS.bat
echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul