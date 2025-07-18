#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client OpenAI pour J.A.R.V.I.S.
Utilisation ponctuelle de ChatGPT avec nouvelle API
"""

import logging
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI library non disponible")

class OpenAIClient:
    def __init__(self, config):
        """Initialisation du client OpenAI"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Configuration OpenAI
        self.api_key = config["openai"]["api_key"]
        self.model = config["openai"]["model"]
        self.client = None
        
        if OPENAI_AVAILABLE and self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self.logger.info("Client OpenAI initialisé")
            except Exception as e:
                self.logger.error(f"Erreur initialisation OpenAI: {e}")
                self.client = None
        else:
            self.logger.warning("Clé API OpenAI non configurée ou bibliothèque manquante")
    
    def is_available(self):
        """Vérifier si OpenAI est disponible"""
        return OPENAI_AVAILABLE and bool(self.api_key) and self.client is not None
    
    def get_response(self, user_input, context=None):
        """Obtenir une réponse de ChatGPT"""
        if not self.is_available():
            if not OPENAI_AVAILABLE:
                return "La bibliothèque OpenAI n'est pas installée. Installez avec: pip install openai"
            return "La fonctionnalité ChatGPT n'est pas configurée. Veuillez ajouter votre clé API OpenAI."
        
        try:
            # Préparer le prompt système
            system_prompt = """Tu es J.A.R.V.I.S., l'assistant personnel intelligent d'Iron Man.
            Tu utilises maintenant les capacités avancées de ChatGPT.
            Réponds en français, de manière précise et professionnelle.
            Tu peux être légèrement sarcastique comme dans les films.
            Adresse-toi à l'utilisateur avec respect ("Monsieur" ou "Madame")."""
            
            # Préparer les messages
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            # Ajouter le contexte si disponible
            if context:
                context_msg = self.format_context(context)
                messages.insert(1, {"role": "system", "content": f"Contexte actuel: {context_msg}"})
            
            # Appel à l'API OpenAI avec nouvelle méthode
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                top_p=0.9
            )
            
            assistant_response = response.choices[0].message.content
            self.logger.info(f"Réponse ChatGPT obtenue: {assistant_response[:100]}...")
            
            return assistant_response
            
        except Exception as e:
            error_msg = str(e).lower()
            
            if "authentication" in error_msg or "api_key" in error_msg:
                self.logger.error("Erreur d'authentification OpenAI")
                return "Erreur d'authentification avec ChatGPT. Vérifiez votre clé API."
            elif "rate_limit" in error_msg or "quota" in error_msg:
                self.logger.error("Limite de taux OpenAI atteinte")
                return "Limite de requêtes ChatGPT atteinte. Veuillez patienter."
            elif "connection" in error_msg or "network" in error_msg:
                self.logger.error(f"Erreur de connexion OpenAI: {e}")
                return "Erreur de connexion avec ChatGPT. Vérifiez votre connexion internet."
            else:
                self.logger.error(f"Erreur OpenAI: {e}")
                return "Erreur technique avec ChatGPT. Veuillez réessayer."
    
    def format_context(self, context):
        """Formater le contexte pour ChatGPT"""
        context_parts = []
        
        if context.get("timestamp"):
            context_parts.append(f"Heure: {context['timestamp']}")
        
        if context.get("screen_data"):
            context_parts.append(f"Écran: {context['screen_data']}")
        
        if context.get("telemetry"):
            telemetry = context["telemetry"]
            context_parts.append(f"Télémétrie: {telemetry}")
        
        if context.get("dcs_active"):
            context_parts.append("Module DCS F/A-18 actif")
        
        if context.get("recent_interactions"):
            context_parts.append("Historique récent disponible")
        
        return " | ".join(context_parts) if context_parts else "Aucun contexte spécifique"
    
    def test_connection(self):
        """Tester la connexion à OpenAI"""
        if not self.is_available():
            return False, "Client OpenAI non disponible"
        
        try:
            # Test simple avec un prompt minimal
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            
            return True, "Connexion OpenAI réussie"
            
        except Exception as e:
            return False, f"Erreur de connexion: {e}"
    
    def set_api_key(self, api_key):
        """Définir la clé API"""
        self.api_key = api_key
        
        if OPENAI_AVAILABLE:
            try:
                self.client = OpenAI(api_key=api_key)
                # Mise à jour du config
                self.config["openai"]["api_key"] = api_key
                self.logger.info("Clé API OpenAI mise à jour")
                return True
            except Exception as e:
                self.logger.error(f"Erreur configuration clé API: {e}")
                return False
        else:
            self.logger.error("Bibliothèque OpenAI non disponible")
            return False
    
    def get_status(self):
        """Obtenir le statut du client"""
        status = {
            "openai_library_available": OPENAI_AVAILABLE,
            "api_key_configured": bool(self.api_key),
            "client_initialized": self.client is not None,
            "model": self.model
        }
        
        if self.is_available():
            connected, message = self.test_connection()
            status["connected"] = connected
            status["connection_message"] = message
        else:
            status["connected"] = False
            if not OPENAI_AVAILABLE:
                status["connection_message"] = "Bibliothèque OpenAI non installée"
            elif not self.api_key:
                status["connection_message"] = "Clé API non configurée"
            else:
                status["connection_message"] = "Client non initialisé"
        
        return status