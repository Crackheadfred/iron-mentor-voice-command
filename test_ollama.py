#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test spécifique pour Ollama
Vérifie si Ollama fonctionne correctement avec des modèles légers
"""

import requests
import json
import sys
import time
import psutil
from pathlib import Path

def check_ollama_service():
    """Vérifier si le service Ollama est actif"""
    print("=== VÉRIFICATION SERVICE OLLAMA ===")
    
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=5)
        if response.status_code == 200:
            version_info = response.json()
            print(f"✅ Ollama actif - Version: {version_info.get('version', 'Inconnue')}")
            return True
        else:
            print(f"❌ Ollama répond avec le code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Ollama n'est pas accessible sur localhost:11434")
        print("   Vérifiez qu'Ollama est démarré")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def check_available_models():
    """Lister les modèles disponibles"""
    print("\n=== MODÈLES DISPONIBLES ===")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                print(f"✅ {len(models)} modèle(s) installé(s):")
                for model in models:
                    name = model.get('name', 'Nom inconnu')
                    size = model.get('size', 0) / (1024**3)  # Conversion en GB
                    print(f"   - {name} ({size:.1f} GB)")
                return models
            else:
                print("⚠️  Aucun modèle installé")
                return []
        else:
            print(f"❌ Erreur {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return []

def test_lightweight_model():
    """Tester avec un modèle léger"""
    print("\n=== TEST MODÈLE LÉGER ===")
    
    # Modèles légers recommandés par ordre de préférence
    lightweight_models = [
        "llama3.2:1b",
        "llama3.2:3b", 
        "gemma2:2b",
        "phi3:mini"
    ]
    
    models = check_available_models()
    model_names = [m.get('name', '') for m in models]
    
    # Trouver le premier modèle léger disponible
    selected_model = None
    for model in lightweight_models:
        if any(model in name for name in model_names):
            selected_model = model
            break
    
    if not selected_model:
        print("❌ Aucun modèle léger trouvé")
        print("Installez un modèle léger avec: ollama pull llama3.2:1b")
        return False
    
    print(f"🧪 Test avec le modèle: {selected_model}")
    
    try:
        # Test simple avec monitoring mémoire
        memory_before = psutil.virtual_memory().percent
        print(f"   Mémoire avant: {memory_before:.1f}%")
        
        payload = {
            "model": selected_model,
            "prompt": "Bonjour",
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_ctx": 1024  # Contexte réduit
            }
        }
        
        print("   Envoi de la requête...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        end_time = time.time()
        memory_after = psutil.virtual_memory().percent
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '')
            
            print(f"✅ Test réussi!")
            print(f"   Temps de réponse: {end_time - start_time:.1f}s")
            print(f"   Mémoire après: {memory_after:.1f}%")
            print(f"   Augmentation mémoire: {memory_after - memory_before:.1f}%")
            print(f"   Réponse: {response_text[:100]}...")
            
            # Alerte si trop de mémoire utilisée
            if memory_after > 85:
                print("⚠️  ATTENTION: Utilisation mémoire élevée!")
                print("   Considérez un modèle encore plus léger")
            
            return True
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - Le modèle met trop de temps à répondre")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def suggest_configuration():
    """Suggérer une configuration optimale"""
    print("\n=== CONFIGURATION RECOMMANDÉE ===")
    
    # Vérifier la RAM disponible
    memory = psutil.virtual_memory()
    total_gb = memory.total / (1024**3)
    available_gb = memory.available / (1024**3)
    
    print(f"RAM totale: {total_gb:.1f} GB")
    print(f"RAM disponible: {available_gb:.1f} GB")
    
    if total_gb < 8:
        print("⚠️  RAM limitée - Utilisez llama3.2:1b")
        recommended_model = "llama3.2:1b"
    elif total_gb < 16:
        print("✅ RAM suffisante - Utilisez llama3.2:3b")
        recommended_model = "llama3.2:3b"
    else:
        print("✅ RAM abondante - Vous pouvez utiliser des modèles plus gros")
        recommended_model = "llama3.2:3b"
    
    # Mettre à jour la configuration si nécessaire
    config_path = Path('config/config.json')
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            current_model = config.get('ollama', {}).get('model', '')
            if current_model != recommended_model:
                print(f"\n📝 Mise à jour recommandée de la configuration:")
                print(f"   Actuel: {current_model}")
                print(f"   Recommandé: {recommended_model}")
                
                config['ollama']['model'] = recommended_model
                config['ollama']['enable_low_memory'] = True
                config['ollama']['context_length'] = 2048
                
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                
                print("✅ Configuration mise à jour!")
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour: {e}")

def main():
    """Fonction principale"""
    print("JARVIS - TEST OLLAMA")
    print("=" * 40)
    
    success = True
    
    # Tests séquentiels
    if not check_ollama_service():
        success = False
        print("\n🔧 SOLUTIONS:")
        print("1. Démarrez Ollama manuellement")
        print("2. Vérifiez qu'il n'y a pas d'erreur au démarrage")
        print("3. Redémarrez votre ordinateur si nécessaire")
        return False
    
    models = check_available_models()
    if not models:
        success = False
        print("\n🔧 SOLUTION:")
        print("Installez un modèle léger: ollama pull llama3.2:1b")
        return False
    
    if not test_lightweight_model():
        success = False
    
    suggest_configuration()
    
    if success:
        print("\n🎉 OLLAMA FONCTIONNE CORRECTEMENT!")
    else:
        print("\n⚠️  PROBLÈMES DÉTECTÉS AVEC OLLAMA")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 ERREUR CRITIQUE: {e}")
        sys.exit(1)