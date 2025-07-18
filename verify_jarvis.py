#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification complète pour J.A.R.V.I.S.
Vérifie que tous les modules et dépendances sont correctement installés
"""

import sys
import json
import traceback
from pathlib import Path

def test_basic_modules():
    """Test des modules Python de base"""
    print("=== TEST DES MODULES DE BASE ===")
    
    basic_modules = [
        'json', 'logging', 'pathlib', 'sqlite3', 'threading', 'queue',
        'datetime', 'time', 'os', 'sys', 'io'
    ]
    
    success = 0
    for module in basic_modules:
        try:
            if module == 'pathlib':
                from pathlib import Path
            else:
                __import__(module)
            print(f"✅ {module}")
            success += 1
        except Exception as e:
            print(f"❌ {module}: {e}")
    
    print(f"Modules de base: {success}/{len(basic_modules)}")
    return success == len(basic_modules)

def test_external_modules():
    """Test des modules externes installés via pip"""
    print("\n=== TEST DES MODULES EXTERNES ===")
    
    external_modules = [
        ('requests', 'requests'),
        ('openai', 'openai'),
        ('numpy', 'numpy'),
        ('torch', 'torch'),
        ('opencv', 'cv2'),
        ('pillow', 'PIL'),
        ('pygame', 'pygame'),
        ('psutil', 'psutil'),
        ('speech_recognition', 'speech_recognition'),
        ('pyttsx3', 'pyttsx3'),
        ('pytesseract', 'pytesseract'),
        ('pyautogui', 'pyautogui'),
        ('TTS', 'TTS'),
    ]
    
    success = 0
    optional_failed = []
    
    for name, import_name in external_modules:
        try:
            if import_name == 'PIL':
                from PIL import Image
            elif import_name == 'cv2':
                import cv2
            else:
                __import__(import_name)
            print(f"✅ {name}")
            success += 1
        except Exception as e:
            if name in ['TTS', 'pyautogui']:  # Modules optionnels
                print(f"⚠️  {name}: {str(e)[:50]} (optionnel)")
                optional_failed.append(name)
            else:
                print(f"❌ {name}: {str(e)[:50]}")
    
    print(f"Modules externes: {success}/{len(external_modules)}")
    if optional_failed:
        print(f"Modules optionnels échoués: {optional_failed}")
    
    return success >= len(external_modules) - len(optional_failed)

def test_jarvis_modules():
    """Test des modules spécifiques à J.A.R.V.I.S."""
    print("\n=== TEST DES MODULES J.A.R.V.I.S. ===")
    
    jarvis_modules = [
        'modules.ollama_client',
        'modules.voice_manager',
        'modules.speech_recognition_module',
        'modules.screen_monitor',
        'modules.memory_manager',
        'modules.simhub_mechanic',
        'modules.dcs_cockpit',
        'modules.openai_client'
    ]
    
    success = 0
    for module in jarvis_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
            success += 1
        except Exception as e:
            print(f"❌ {module}: {str(e)[:50]}")
            if "Tortoise" in str(e):
                print("   (Erreur Tortoise TTS - fallback Windows TTS disponible)")
    
    print(f"Modules J.A.R.V.I.S.: {success}/{len(jarvis_modules)}")
    return success >= len(jarvis_modules) - 2  # Tolérer 2 échecs

def test_configuration():
    """Vérifier la configuration"""
    print("\n=== TEST DE LA CONFIGURATION ===")
    
    config_path = Path('config/config.json')
    if not config_path.exists():
        print("❌ Fichier config/config.json manquant")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_sections = ['ollama', 'voice', 'screen', 'openai']
        for section in required_sections:
            if section in config:
                print(f"✅ Section {section}")
            else:
                print(f"❌ Section {section} manquante")
        
        print("✅ Configuration chargée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur configuration: {e}")
        return False

def test_voice_config():
    """Vérifier la configuration de la voix William"""
    print("\n=== TEST CONFIGURATION VOIX WILLIAM ===")
    
    william_path = Path('voices/william')
    if not william_path.exists():
        print("❌ Dossier voices/william manquant")
        return False
    
    voice_config_path = william_path / 'voice_config.json'
    if not voice_config_path.exists():
        print("❌ Fichier voice_config.json manquant")
        return False
    
    try:
        with open(voice_config_path, 'r', encoding='utf-8') as f:
            voice_config = json.load(f)
        print("✅ Configuration voix William")
        return True
    except Exception as e:
        print(f"❌ Erreur config voix: {e}")
        return False

def test_directories():
    """Vérifier les dossiers nécessaires"""
    print("\n=== TEST DES DOSSIERS ===")
    
    required_dirs = [
        'logs', 'memory', 'screenshots', 'config', 
        'voices', 'voices/william', 'logs/telemetry', 'modules'
    ]
    
    success = 0
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}")
            success += 1
        else:
            print(f"❌ {dir_path} manquant")
    
    return success == len(required_dirs)

def test_audio_system():
    """Test du système audio"""
    print("\n=== TEST SYSTÈME AUDIO ===")
    
    try:
        import speech_recognition as sr
        import pyttsx3
        import pygame
        
        # Test microphone
        try:
            r = sr.Recognizer()
            m = sr.Microphone()
            print("✅ Microphone détecté")
        except Exception as e:
            print(f"⚠️  Microphone: {e}")
        
        # Test TTS
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            if voices:
                print(f"✅ TTS Windows - {len(voices)} voix disponibles")
            engine.stop()
        except Exception as e:
            print(f"❌ TTS Windows: {e}")
        
        # Test pygame audio
        try:
            pygame.mixer.init()
            print("✅ Pygame audio")
            pygame.mixer.quit()
        except Exception as e:
            print(f"❌ Pygame audio: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Système audio: {e}")
        return False

def test_cuda_support():
    """Test du support CUDA"""
    print("\n=== TEST SUPPORT CUDA ===")
    
    try:
        import torch
        
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            device_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0)
            print(f"✅ CUDA disponible - {device_count} GPU(s)")
            print(f"   GPU principal: {device_name}")
        else:
            print("⚠️  CUDA non disponible - utilisation CPU")
        
        return True
        
    except Exception as e:
        print(f"❌ Test CUDA: {e}")
        return False

def main():
    """Fonction principale de vérification"""
    print("J.A.R.V.I.S. - VÉRIFICATION COMPLÈTE")
    print("=" * 50)
    
    tests = [
        ("Modules de base", test_basic_modules),
        ("Modules externes", test_external_modules),
        ("Modules J.A.R.V.I.S.", test_jarvis_modules),
        ("Configuration", test_configuration),
        ("Configuration voix", test_voice_config),
        ("Dossiers", test_directories),
        ("Système audio", test_audio_system),
        ("Support CUDA", test_cuda_support),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERREUR lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé final
    print("\n" + "=" * 50)
    print("RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    success_count = 0
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\nRésultat global: {success_count}/{len(results)} tests réussis")
    
    if success_count >= len(results) - 1:  # Tolérer 1 échec
        print("\n🎉 J.A.R.V.I.S. EST PRÊT À FONCTIONNER!")
        return True
    else:
        print(f"\n⚠️  Installation incomplète - {len(results) - success_count} problèmes détectés")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 ERREUR CRITIQUE: {e}")
        traceback.print_exc()
        sys.exit(1)