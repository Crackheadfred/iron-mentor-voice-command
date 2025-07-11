#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de configuration et test pour J.A.R.V.I.S.
Utilitaire de diagnostic et configuration
"""

import sys
import os
import json
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Vérifier la version Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ requis")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Vérifier les dépendances Python"""
    required_modules = [
        'requests', 'openai', 'speech_recognition', 'pyttsx3', 
        'pygame', 'cv2', 'pytesseract', 'PIL', 'psutil',
        'torch', 'numpy'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing.append(module)
    
    return len(missing) == 0, missing

def check_cuda():
    """Vérifier CUDA"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✅ CUDA disponible - GPU: {gpu_name} ({gpu_count} GPU(s))")
            return True
        else:
            print("⚠️ CUDA non disponible")
            return False
    except ImportError:
        print("❌ PyTorch non installé")
        return False

def check_ollama():
    """Vérifier Ollama"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            model_names = [model["name"] for model in models.get("models", [])]
            print(f"✅ Ollama connecté - Modèles: {len(model_names)}")
            
            if "mistral-small3.2:24b" in model_names:
                print("✅ Modèle mistral-small3.2:24b disponible")
                return True
            else:
                print("⚠️ Modèle mistral-small3.2:24b non trouvé")
                print("   Installez avec: ollama pull mistral-small3.2:24b")
                return False
        else:
            print("❌ Ollama erreur de connexion")
            return False
    except Exception as e:
        print(f"❌ Ollama non accessible: {e}")
        return False

def check_tesseract():
    """Vérifier Tesseract OCR"""
    try:
        # Tenter d'importer pytesseract
        import pytesseract
        
        # Chemins possibles pour Tesseract
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            "tesseract"
        ]
        
        for path in possible_paths:
            try:
                pytesseract.pytesseract.tesseract_cmd = path
                # Test simple
                from PIL import Image
                test_image = Image.new('RGB', (100, 50), color='white')
                pytesseract.image_to_string(test_image)
                print(f"✅ Tesseract trouvé: {path}")
                return True
            except:
                continue
        
        print("❌ Tesseract non trouvé")
        print("   Installez depuis: https://github.com/UB-Mannheim/tesseract/wiki")
        return False
        
    except ImportError:
        print("❌ pytesseract non installé")
        return False

def check_audio():
    """Vérifier les capacités audio"""
    try:
        import speech_recognition as sr
        import pyttsx3
        
        # Test microphone
        r = sr.Recognizer()
        mic_list = sr.Microphone.list_microphone_names()
        print(f"✅ Reconnaissance vocale - {len(mic_list)} microphone(s)")
        
        # Test TTS
        tts = pyttsx3.init()
        voices = tts.getProperty('voices')
        print(f"✅ Synthèse vocale - {len(voices)} voix disponibles")
        
        return True
    except Exception as e:
        print(f"❌ Audio: {e}")
        return False

def create_directories():
    """Créer les répertoires nécessaires"""
    directories = [
        "logs", "memory", "screenshots", 
        "voices/william", "logs/telemetry", "config"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ Répertoires créés")

def create_default_config():
    """Créer la configuration par défaut"""
    config_path = Path("config/config.json")
    
    if not config_path.exists():
        default_config = {
            "ollama": {
                "model": "mistral-small3.2:24b",
                "url": "http://localhost:11434"
            },
            "openai": {
                "api_key": "",
                "model": "gpt-4"
            },
            "voice": {
                "william_voice_path": "voices/william/",
                "tts_engine": "tortoise"
            },
            "screen": {
                "ocr_enabled": True,
                "monitoring_interval": 2
            },
            "simhub": {
                "enabled": True,
                "port": 8888
            },
            "dcs": {
                "enabled": True,
                "aircraft": "F/A-18C"
            }
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        print("✅ Configuration par défaut créée")
    else:
        print("✅ Configuration existante trouvée")

def test_jarvis_import():
    """Tester l'import des modules J.A.R.V.I.S."""
    try:
        # Test des imports principaux
        from modules.voice_manager import VoiceManager
        from modules.ollama_client import OllamaClient
        from modules.memory_manager import MemoryManager
        
        print("✅ Modules J.A.R.V.I.S. importables")
        return True
    except Exception as e:
        print(f"❌ Erreur import modules: {e}")
        return False

def run_quick_test():
    """Test rapide de fonctionnement"""
    try:
        # Test basique de chaque composant
        print("\n🧪 Test rapide des composants...")
        
        # Test Ollama
        from modules.ollama_client import OllamaClient
        config = {"ollama": {"model": "mistral-small3.2:24b", "url": "http://localhost:11434"}}
        ollama = OllamaClient(config)
        print("✅ Client Ollama initialisé")
        
        # Test mémoire
        from modules.memory_manager import MemoryManager
        memory = MemoryManager()
        memory.add_interaction("system", "Test de fonctionnement")
        print("✅ Gestionnaire mémoire fonctionnel")
        
        print("✅ Tests rapides réussis")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        return False

def main():
    """Fonction principale de diagnostic"""
    print("🤖 J.A.R.V.I.S. - Diagnostic et Configuration")
    print("=" * 50)
    
    # Vérifications système
    print("\n🔍 Vérifications système:")
    python_ok = check_python_version()
    deps_ok, missing = check_dependencies()
    cuda_ok = check_cuda()
    
    # Vérifications services
    print("\n🔍 Vérifications services:")
    ollama_ok = check_ollama()
    tesseract_ok = check_tesseract()
    audio_ok = check_audio()
    
    # Configuration
    print("\n⚙️ Configuration:")
    create_directories()
    create_default_config()
    
    # Tests
    print("\n🧪 Tests modules:")
    import_ok = test_jarvis_import()
    
    if import_ok and ollama_ok:
        test_ok = run_quick_test()
    else:
        test_ok = False
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 50)
    
    all_checks = [
        ("Python 3.8+", python_ok),
        ("Dépendances Python", deps_ok),
        ("CUDA", cuda_ok),
        ("Ollama + Mistral", ollama_ok),
        ("Tesseract OCR", tesseract_ok),
        ("Système Audio", audio_ok),
        ("Modules J.A.R.V.I.S.", import_ok),
        ("Tests fonctionnels", test_ok if 'test_ok' in locals() else False)
    ]
    
    passed = sum(1 for _, status in all_checks if status)
    total = len(all_checks)
    
    for name, status in all_checks:
        icon = "✅" if status else "❌"
        print(f"{icon} {name}")
    
    print(f"\n🎯 Score: {passed}/{total}")
    
    if passed == total:
        print("🎉 Tous les tests passés! J.A.R.V.I.S. est prêt.")
        print("   Lancez avec: START_JARVIS.bat")
    elif passed >= 6:
        print("⚠️ Configuration partielle. J.A.R.V.I.S. peut fonctionner avec des limitations.")
    else:
        print("❌ Configuration insuffisante. Corrigez les erreurs avant de lancer J.A.R.V.I.S.")
    
    # Actions recommandées
    if not deps_ok:
        print(f"\n📦 Dépendances manquantes: {', '.join(missing)}")
        print("   Exécutez: pip install -r requirements.txt")
    
    if not ollama_ok:
        print("\n🤖 Ollama requis:")
        print("   1. Installez Ollama: https://ollama.ai/")
        print("   2. Démarrez: ollama serve")
        print("   3. Installez le modèle: ollama pull mistral-small3.2:24b")
    
    if not tesseract_ok:
        print("\n👁️ Tesseract OCR requis pour l'analyse d'écran:")
        print("   Installez: https://github.com/UB-Mannheim/tesseract/wiki")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()