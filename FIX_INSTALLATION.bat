@echo off
chcp 65001 > nul
echo ========================================
echo RÉPARATION J.A.R.V.I.S.
echo ========================================
echo.

:: Aller dans le répertoire du projet
cd /d "%~dp0"

:: Vérifier si l'environnement virtuel existe
if not exist "jarvis_env" (
    echo ERREUR: Environnement virtuel non trouvé
    echo Relancez INSTALL_JARVIS.bat
    pause
    exit /b 1
)

:: Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call jarvis_env\Scripts\activate.bat

:: Vérifier que l'environnement est activé
echo Vérification de l'environnement Python...
python -c "import sys; print('Python:', sys.executable)"
echo.

:: Installer les dépendances avec pip dans l'environnement virtuel
echo Installation des dépendances dans l'environnement virtuel...
python -m pip install --upgrade pip
echo.

:: Installation forcée des modules principaux
echo Installation des modules de base...
python -m pip install requests>=2.31.0
python -m pip install openai>=1.40.0
python -m pip install SpeechRecognition>=3.10.0
python -m pip install pyttsx3>=2.90
python -m pip install psutil>=5.9.0
echo.

:: Installation des modules d'image/vision
echo Installation des modules vision...
python -m pip install pytesseract>=0.3.10
python -m pip install Pillow>=10.0.0
python -m pip install pyautogui>=0.9.54
python -m pip install opencv-python>=4.9.0
echo.

:: Installation NumPy spécifique
echo Installation NumPy...
python -m pip install --only-binary=all "numpy>=1.21.0,<2.0.0"
echo.

:: Installation modules audio (optionnels)
echo Installation modules audio...
python -m pip install pygame || echo ATTENTION: pygame optionnel
python -m pip install pyaudio || echo ATTENTION: pyaudio optionnel
echo.

:: Test final
echo ========================================
echo TEST DES MODULES
echo ========================================
python -c "
import sys
modules = ['requests', 'openai', 'speech_recognition', 'pyttsx3', 'psutil', 'pytesseract', 'PIL', 'cv2', 'numpy']
success = 0
total = len(modules)

for module in modules:
    try:
        __import__(module)
        print(f'✓ {module}')
        success += 1
    except ImportError as e:
        print(f'✗ {module} - {e}')

print(f'\nScore: {success}/{total}')
if success == total:
    print('SUCCÈS: Tous les modules sont installés!')
else:
    print('ATTENTION: Certains modules manquent')
"

echo.
echo ========================================
echo RÉPARATION TERMINÉE
echo ========================================
echo.
echo Pour tester J.A.R.V.I.S.:
echo 1. Lancez DIAGNOSTIC_JARVIS.bat
echo 2. Si OK, lancez START_JARVIS.bat
echo.
pause