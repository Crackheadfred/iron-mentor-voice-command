#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de reconnaissance vocale pour J.A.R.V.I.S.
"""

import logging
import speech_recognition as sr
import pyaudio
import threading
import queue
import time
from pathlib import Path

class SpeechRecognitionModule:
    def __init__(self, config):
        """Initialisation du module de reconnaissance vocale"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialisation du recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = None
        
        # Configuration
        self.language = "fr-FR"  # Français
        self.energy_threshold = 4000
        self.dynamic_energy_threshold = True
        self.pause_threshold = 0.8
        
        # Queue pour les commandes audio
        self.audio_queue = queue.Queue()
        self.listening = False
        
        self.setup_microphone()
        self.logger.info("Module de reconnaissance vocale initialisé")
    
    def setup_microphone(self):
        """Configuration du microphone"""
        try:
            # Obtenir la liste des microphones
            mic_list = sr.Microphone.list_microphone_names()
            self.logger.info(f"Microphones disponibles: {mic_list}")
            
            # Utiliser le microphone par défaut
            self.microphone = sr.Microphone()
            
            # Calibrage du microphone
            with self.microphone as source:
                self.logger.info("Calibrage du microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
            self.recognizer.energy_threshold = self.energy_threshold
            self.recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold
            self.recognizer.pause_threshold = self.pause_threshold
            
            self.logger.info("Microphone configuré avec succès")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la configuration du microphone: {e}")
            self.microphone = None
    
    def listen_continuously(self):
        """Écoute continue en arrière-plan"""
        def callback(recognizer, audio):
            try:
                # Reconnaissance vocale
                text = recognizer.recognize_google(audio, language=self.language)
                self.audio_queue.put(text)
                self.logger.info(f"Audio détecté: {text}")
            except sr.UnknownValueError:
                # Pas de parole détectée
                pass
            except sr.RequestError as e:
                self.logger.error(f"Erreur de reconnaissance vocale: {e}")
        
        # Démarrer l'écoute continue
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, callback, phrase_time_limit=5
        )
        
        self.listening = True
        self.logger.info("Écoute continue démarrée")
    
    def listen(self, timeout=1):
        """Écouter une commande vocale (méthode synchrone)"""
        if not self.microphone:
            return None
        
        try:
            with self.microphone as source:
                # Réduire le timeout pour être plus réactif
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
            
            # Reconnaissance vocale
            text = self.recognizer.recognize_google(audio, language=self.language)
            self.logger.info(f"✅ Commande reconnue: {text}")
            return text
            
        except sr.WaitTimeoutError:
            # Timeout - normal, ne pas log
            return None
        except sr.UnknownValueError:
            # Pas de parole claire détectée - normal
            return None
        except sr.RequestError as e:
            # Erreur de service - log uniquement si pas d'internet
            if "connection" in str(e).lower():
                self.logger.warning("Pas de connexion internet pour la reconnaissance vocale")
            else:
                self.logger.error(f"Erreur de reconnaissance vocale: {e}")
            return None
        except OSError as e:
            # Erreur microphone
            self.logger.error(f"Erreur microphone: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Erreur inattendue lors de l'écoute: {e}")
            return None
    
    def get_pending_commands(self):
        """Récupérer les commandes en attente (écoute continue)"""
        commands = []
        try:
            while not self.audio_queue.empty():
                commands.append(self.audio_queue.get_nowait())
        except queue.Empty:
            pass
        return commands
    
    def start_continuous_listening(self):
        """Démarrer l'écoute continue"""
        if not self.listening and self.microphone:
            thread = threading.Thread(target=self.listen_continuously, daemon=True)
            thread.start()
    
    def stop_continuous_listening(self):
        """Arrêter l'écoute continue"""
        if hasattr(self, 'stop_listening') and self.stop_listening:
            self.stop_listening(wait_for_stop=False)
            self.listening = False
            self.logger.info("Écoute continue arrêtée")
    
    def test_microphone(self):
        """Tester le microphone"""
        if not self.microphone:
            return False, "Microphone non disponible"
        
        try:
            with self.microphone as source:
                self.logger.info("Test du microphone... Dites quelque chose.")
                audio = self.recognizer.listen(source, timeout=5)
                
            text = self.recognizer.recognize_google(audio, language=self.language)
            return True, f"Test réussi. Texte reconnu: {text}"
            
        except Exception as e:
            return False, f"Échec du test: {e}"
    
    def calibrate_microphone(self):
        """Recalibrer le microphone"""
        if not self.microphone:
            return False
        
        try:
            with self.microphone as source:
                self.logger.info("Recalibrage du microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=3)
                
            self.logger.info(f"Nouveau seuil d'énergie: {self.recognizer.energy_threshold}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors du calibrage: {e}")
            return False
    
    def get_status(self):
        """Obtenir le statut du module"""
        return {
            "microphone_available": self.microphone is not None,
            "listening": self.listening,
            "energy_threshold": self.recognizer.energy_threshold if self.recognizer else None,
            "language": self.language,
            "pending_commands": self.audio_queue.qsize()
        }