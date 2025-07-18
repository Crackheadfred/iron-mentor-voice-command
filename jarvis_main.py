#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
J.A.R.V.I.S. - Assistant Vocal Intelligent Local
Module principal de gestion
"""

import os
import sys
import json
import threading
import time
import logging
from datetime import datetime
from pathlib import Path

# Modules internes
from modules.voice_manager import VoiceManager
from modules.speech_recognition_module import SpeechRecognitionModule
from modules.ollama_client import OllamaClient
from modules.openai_client import OpenAIClient
from modules.screen_monitor import ScreenMonitor
from modules.simhub_mechanic import SimHubMechanic
from modules.dcs_cockpit import DCSCockpit
from modules.memory_manager import MemoryManager

class JARVIS:
    def __init__(self):
        """Initialisation de J.A.R.V.I.S."""
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Configuration
        self.config = self.load_config()
        self.is_active = True
        self.is_silent = False
        self.current_voice = "William"  # William ou Windows
        
        # Initialisation des modules
        self.memory_manager = MemoryManager()
        self.voice_manager = VoiceManager(self.config)
        self.speech_recognition = SpeechRecognitionModule(self.config)
        self.ollama_client = OllamaClient(self.config)
        self.openai_client = OpenAIClient(self.config)
        self.screen_monitor = ScreenMonitor(self.config)
        self.simhub_mechanic = SimHubMechanic(self.config)
        self.dcs_cockpit = DCSCockpit(self.config)
        
        # Commandes d'activation/désactivation
        self.activation_phrases = [
            "jarvis", "j.a.r.v.i.s", "t'es là", "prêt pour mes commandes",
            "jarvis t'es là", "j.a.r.v.i.s. t'es là", "prêt pour mes commandes jarvis"
        ]
        
        self.silence_phrases = [
            "silence", "c'est beau", "tais-toi", "stop"
        ]
        
        self.logger.info("J.A.R.V.I.S. initialisé avec succès")
        
    def setup_logging(self):
        """Configuration du système de logs"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"logs/jarvis_{datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler()
            ]
        )
    
    def load_config(self):
        """Chargement de la configuration"""
        config_path = Path("config/config.json")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Configuration par défaut
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
            
            # Créer le répertoire de config et sauvegarder
            config_path.parent.mkdir(exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            
            return default_config
    
    def speak(self, text):
        """Faire parler J.A.R.V.I.S."""
        if not self.is_silent:
            self.voice_manager.speak(text, voice=self.current_voice)
            self.logger.info(f"J.A.R.V.I.S. dit: {text}")
    
    def listen(self):
        """Écouter les commandes vocales"""
        try:
            return self.speech_recognition.listen()
        except Exception as e:
            self.logger.error(f"Erreur lors de l'écoute: {e}")
            return None
    
    def process_command(self, command):
        """Traiter une commande vocale ou textuelle"""
        if not command:
            return
            
        command_lower = command.lower()
        self.logger.info(f"Commande reçue: {command}")
        
        # Sauvegarde en mémoire
        self.memory_manager.add_interaction("user", command)
        
        # Commandes de contrôle système
        if any(phrase in command_lower for phrase in self.silence_phrases):
            self.is_silent = True
            self.speak("Mode silencieux activé.")
            return
            
        if any(phrase in command_lower for phrase in self.activation_phrases) and self.is_silent:
            self.is_silent = False
            self.speak("Je suis là, monsieur. Prêt pour vos commandes.")
            return
            
        # Commandes de changement de voix
        if "change de voix" in command_lower or "voix windows" in command_lower:
            self.current_voice = "Windows" if self.current_voice == "William" else "William"
            self.speak(f"Voix changée vers {self.current_voice}")
            return
            
        # Commandes spécifiques aux modules
        if "utilise chatgpt" in command_lower:
            response = self.openai_client.get_response(command)
            self.speak(response)
            self.memory_manager.add_interaction("jarvis", response)
            return
            
        if "analyse l'écran" in command_lower:
            screen_data = self.screen_monitor.analyze_screen()
            response = f"Je vois: {screen_data}"
            self.speak(response)
            return
            
        if "analyse mon tour" in command_lower:
            telemetry = self.simhub_mechanic.get_telemetry_advice()
            self.speak(telemetry)
            return
            
        if "active le module f-18" in command_lower or "module dcs" in command_lower:
            self.dcs_cockpit.activate()
            self.speak("Module F/A-18 activé. Je suis prêt à vous assister.")
            return
            
        if self.dcs_cockpit.is_active and ("comment" in command_lower or "prépare" in command_lower):
            response = self.dcs_cockpit.handle_command(command)
            self.speak(response)
            return
        
        # Commande générale - utiliser Ollama
        try:
            context = self.get_context()
            response = self.ollama_client.get_response(command, context)
            self.speak(response)
            self.memory_manager.add_interaction("jarvis", response)
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement: {e}")
            self.speak("Désolé, j'ai rencontré une erreur lors du traitement de votre demande.")
    
    def get_context(self):
        """Obtenir le contexte actuel (écran, télémétrie, etc.)"""
        context = {
            "timestamp": datetime.now().isoformat(),
            "screen_active": self.screen_monitor.is_monitoring,
            "dcs_active": self.dcs_cockpit.is_active,
            "recent_interactions": self.memory_manager.get_recent_interactions(5)
        }
        
        # Ajouter données d'écran si disponibles
        if self.screen_monitor.is_monitoring:
            context["screen_data"] = self.screen_monitor.get_current_screen_text()
        
        # Ajouter données de télémétrie si disponibles
        if self.simhub_mechanic.is_connected():
            context["telemetry"] = self.simhub_mechanic.get_current_telemetry()
            
        return context
    
    def start_background_monitoring(self):
        """Démarrer la surveillance en arrière-plan"""
        def monitor_screen():
            while self.is_active:
                if self.screen_monitor.is_monitoring:
                    self.screen_monitor.update_screen_data()
                time.sleep(2)
        
        def monitor_simhub():
            while self.is_active:
                if self.simhub_mechanic.is_connected():
                    self.simhub_mechanic.update_telemetry()
                time.sleep(0.5)
        
        # Démarrer les threads de surveillance
        threading.Thread(target=monitor_screen, daemon=True).start()
        threading.Thread(target=monitor_simhub, daemon=True).start()
        
        self.logger.info("Surveillance en arrière-plan démarrée")
    
    def run(self):
        """Boucle principale de J.A.R.V.I.S."""
        self.speak("J.A.R.V.I.S. en ligne. Tous les systèmes opérationnels.")
        
        # Démarrer la surveillance en arrière-plan
        self.start_background_monitoring()
        
        # Activer l'analyse d'écran par défaut
        self.screen_monitor.start_monitoring()
        
        try:
            while self.is_active:
                # Écoute vocale
                command = self.listen()
                if command:
                    self.process_command(command)
                
                # Écoute clavier (Windows compatible)
                try:
                    if hasattr(sys, '_getframe'):  # Windows
                        import msvcrt
                        if msvcrt.kbhit():
                            keyboard_input = input().strip()
                            if keyboard_input:
                                self.process_command(keyboard_input)
                    else:  # Linux/Mac
                        if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                            keyboard_input = input().strip()
                            if keyboard_input:
                                self.process_command(keyboard_input)
                except:
                    pass  # Ignorer les erreurs de clavier
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            self.logger.info("Arrêt de J.A.R.V.I.S. demandé")
            self.speak("Au revoir, monsieur.")
            self.is_active = False
        except Exception as e:
            self.logger.error(f"Erreur critique: {e}")
            self.speak("Erreur système critique. Arrêt d'urgence.")
            self.is_active = False

if __name__ == "__main__":
    try:
        import select
    except ImportError:
        # Pour Windows
        import msvcrt
        
        def check_keyboard():
            if msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8')
            return None
    
    jarvis = JARVIS()
    jarvis.run()