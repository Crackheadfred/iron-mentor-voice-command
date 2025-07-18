#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client Ollama pour J.A.R.V.I.S.
Communication avec le modèle Mistral local
"""

import requests
import json
import logging
from datetime import datetime
import time
import torch

class OllamaClient:
    def __init__(self, config):
        """Initialisation du client Ollama"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        self.base_url = config["ollama"]["url"]
        self.model = config["ollama"]["model"]
        
        # Personnalité de J.A.R.V.I.S.
        self.system_prompt = """Tu es J.A.R.V.I.S., l'assistant personnel intelligent d'Iron Man.
        Tu es poli, professionnel, légèrement sarcastique parfois, et très compétent.
        Tu t'adresses à ton utilisateur avec respect ("Monsieur" ou "Madame").
        Tu es capable d'analyser des situations complexes et de fournir des conseils techniques.
        Tu peux aider avec la programmation, les jeux de simulation, l'aviation, et bien d'autres sujets.
        Réponds toujours en français, de manière concise mais complète.
        Si tu n'es pas sûr de quelque chose, dis-le clairement."""
        
        self.conversation_history = []
        self.max_history = 20
        
        # Test de connexion
        self.test_connection()
        
    def test_connection(self):
        """Tester la connexion à Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json()
                model_names = [model["name"] for model in models.get("models", [])]
                
                if self.model in model_names:
                    self.logger.info(f"Connexion Ollama réussie. Modèle {self.model} disponible.")
                    return True
                else:
                    self.logger.warning(f"Modèle {self.model} non trouvé. Modèles disponibles: {model_names}")
            else:
                self.logger.error(f"Erreur Ollama: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.logger.error("Impossible de se connecter à Ollama. Vérifiez qu'Ollama est démarré.")
        except Exception as e:
            self.logger.error(f"Erreur lors du test de connexion Ollama: {e}")
            
        return False
    
    def get_response(self, user_input, context=None):
        """Obtenir une réponse du modèle Mistral"""
        try:
            print(f"🔄 Début traitement Ollama...")
            
            # Test de connexion rapide
            if not self.test_connection():
                print("❌ Connexion Ollama échouée")
                return "Désolé monsieur, je ne parviens pas à accéder à mon processeur principal."
            
            # Préparer le prompt avec contexte
            full_prompt = self.prepare_prompt(user_input, context)
            print(f"📝 Prompt préparé: {full_prompt[:100]}...")
            
            # Préparer la requête
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    *self.conversation_history[-self.max_history:],
                    {"role": "user", "content": full_prompt}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 300,  # Réduction pour vitesse
                    "num_predict": 300,
                    "repeat_penalty": 1.1,
                    "num_ctx": 2048,    # Contexte plus petit = plus rapide
                    "num_gpu": -1 if torch.cuda.is_available() else 0  # Utiliser GPU si disponible
                }
            }
            
            print(f"🚀 Envoi requête à Ollama...")
            
            # Envoi de la requête
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=30
            )
            
            print(f"📨 Réponse reçue - Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                assistant_response = result["message"]["content"]
                
                print(f"✅ Réponse obtenue: {assistant_response[:100]}...")
                
                # Ajouter à l'historique
                self.conversation_history.append({"role": "user", "content": user_input})
                self.conversation_history.append({"role": "assistant", "content": assistant_response})
                
                # Limiter l'historique
                if len(self.conversation_history) > self.max_history * 2:
                    self.conversation_history = self.conversation_history[-self.max_history:]
                
                self.logger.info(f"Réponse Ollama obtenue: {assistant_response[:100]}...")
                return assistant_response
                
            else:
                error_msg = f"Erreur HTTP {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                self.logger.error(error_msg)
                return "Désolé, je rencontre des difficultés techniques avec mon processeur principal."
                
        except requests.exceptions.Timeout:
            error_msg = "Timeout lors de la requête Ollama"
            print(f"⏰ {error_msg}")
            self.logger.error(error_msg)
            return "Désolé monsieur, le temps de traitement a été dépassé."
            
        except requests.exceptions.ConnectionError:
            error_msg = "Impossible de se connecter à Ollama"
            print(f"🔌 {error_msg}")
            self.logger.error(error_msg)
            return "Je ne parviens pas à me connecter à Ollama. Vérifiez qu'il est démarré."
            
        except Exception as e:
            error_msg = f"Erreur lors de la requête Ollama: {e}"
            print(f"💥 {error_msg}")
            self.logger.error(error_msg)
            return "Je rencontre une erreur technique. Veuillez réessayer."
    
    def prepare_prompt(self, user_input, context=None):
        """Préparer le prompt avec le contexte"""
        prompt = user_input
        
        if context:
            context_info = []
            
            # Ajouter l'heure
            context_info.append(f"Heure actuelle: {datetime.now().strftime('%H:%M:%S')}")
            
            # Ajouter les données d'écran si disponibles
            if context.get("screen_data"):
                context_info.append(f"Contenu de l'écran: {context['screen_data']}")
            
            # Ajouter les données de télémétrie si disponibles
            if context.get("telemetry"):
                telemetry = context["telemetry"]
                context_info.append(f"Télémétrie course: Vitesse: {telemetry.get('speed', 'N/A')} km/h")
            
            # Ajouter l'état des modules
            if context.get("dcs_active"):
                context_info.append("Module DCS F/A-18 actif")
            
            if context_info:
                prompt = f"[CONTEXTE: {' | '.join(context_info)}]\n\nQuestion: {user_input}"
        
        return prompt
    
    def get_models(self):
        """Obtenir la liste des modèles disponibles"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json()
                return [model["name"] for model in models.get("models", [])]
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des modèles: {e}")
        
        return []
    
    def switch_model(self, model_name):
        """Changer de modèle"""
        available_models = self.get_models()
        if model_name in available_models:
            self.model = model_name
            self.logger.info(f"Modèle changé vers: {model_name}")
            return True
        else:
            self.logger.warning(f"Modèle {model_name} non disponible")
            return False
    
    def clear_history(self):
        """Effacer l'historique de conversation"""
        self.conversation_history = []
        self.logger.info("Historique de conversation effacé")
    
    def get_status(self):
        """Obtenir le statut du client"""
        return {
            "connected": self.test_connection(),
            "model": self.model,
            "base_url": self.base_url,
            "history_length": len(self.conversation_history),
            "available_models": self.get_models()
        }