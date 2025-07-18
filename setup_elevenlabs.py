#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de configuration ElevenLabs pour J.A.R.V.I.S.
Configure et teste l'API ElevenLabs
"""

import json
import os
from pathlib import Path
from modules.elevenlabs_client import ElevenLabsClient, FRENCH_VOICES

def configure_elevenlabs():
    """Configure ElevenLabs pour JARVIS"""
    print("=" * 50)
    print("CONFIGURATION ELEVENLABS POUR J.A.R.V.I.S.")
    print("=" * 50)
    print()
    
    # Demander la clé API
    print("1. Obtenez votre clé API sur https://elevenlabs.io")
    print("2. Créez un compte et allez dans votre dashboard")
    print("3. Copiez votre clé API")
    print()
    
    api_key = input("Entrez votre clé API ElevenLabs: ").strip()
    
    if not api_key:
        print("❌ Clé API requise")
        return False
    
    # Tester la connexion
    print("\n🧪 Test de la connexion...")
    client = ElevenLabsClient(api_key)
    
    if not client.test_connection():
        print("❌ Impossible de se connecter à ElevenLabs")
        print("Vérifiez votre clé API et votre connexion internet")
        return False
    
    print("✅ Connexion réussie!")
    
    # Afficher les voix disponibles
    print("\n🎤 Voix françaises recommandées pour JARVIS:")
    print("\nVoix masculines:")
    for name, voice_id in FRENCH_VOICES["masculine"].items():
        print(f"  - {name} ({voice_id})")
    
    print("\nVoix féminines:")
    for name, voice_id in FRENCH_VOICES["feminine"].items():
        print(f"  - {name} ({voice_id})")
    
    # Choisir la voix
    print("\nChoisissez une voix:")
    print("1. Callum (masculine, recommandée)")
    print("2. Liam (masculine)")
    print("3. George (masculine)")
    print("4. Aria (féminine)")
    print("5. Sarah (féminine)")
    print("6. Charlotte (féminine)")
    
    choice = input("\nVotre choix (1-6, défaut=1): ").strip()
    
    voice_mapping = {
        "1": ("Callum", "N2lVS1w4EtoT3dr4eOWO"),
        "2": ("Liam", "TX3LPaxmHKxFdv7VOQHJ"),
        "3": ("George", "JBFqnCBsd6RMkjVDRZzb"),
        "4": ("Aria", "9BWtsMINqrJLrRacOk9x"),
        "5": ("Sarah", "EXAVITQu4vr4xnSDxMaL"),
        "6": ("Charlotte", "XB0fDUnXU5powFXDhCwa")
    }
    
    if choice not in voice_mapping:
        choice = "1"  # Défaut
    
    voice_name, voice_id = voice_mapping[choice]
    print(f"\n✅ Voix sélectionnée: {voice_name}")
    
    # Test de la voix
    print("\n🧪 Test de la voix...")
    client.voice_id = voice_id
    
    test_text = "Bonjour, je suis JARVIS, votre assistant personnel. Comment puis-je vous aider aujourd'hui ?"
    
    if client.speak(test_text):
        print("✅ Test vocal réussi!")
    else:
        print("⚠️  Problème avec l'audio, mais la voix est configurée")
    
    # Sauvegarder la configuration
    config_path = Path('config/config.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config['voice']['elevenlabs_api_key'] = api_key
        config['voice']['voice_id'] = voice_id
        config['voice']['voice_name'] = voice_name
        config['voice']['tts_engine'] = "elevenlabs"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("\n✅ Configuration sauvegardée!")
        print(f"   Moteur TTS: ElevenLabs")
        print(f"   Voix: {voice_name}")
        print(f"   Langue: Français")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la sauvegarde: {e}")
        return False

def main():
    """Fonction principale"""
    try:
        success = configure_elevenlabs()
        
        if success:
            print("\n🎉 ELEVENLABS CONFIGURÉ AVEC SUCCÈS!")
            print("\nJ.A.R.V.I.S. utilisera maintenant ElevenLabs pour la synthèse vocale.")
            print("Vous pouvez démarrer JARVIS avec: demarrer.bat")
        else:
            print("\n⚠️  Configuration incomplète")
            print("Relancez ce script pour réessayer")
            
    except KeyboardInterrupt:
        print("\n\nConfiguration annulée par l'utilisateur")
    except Exception as e:
        print(f"\n💥 ERREUR: {e}")

if __name__ == "__main__":
    main()