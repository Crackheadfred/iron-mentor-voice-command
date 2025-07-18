#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion vocale pour J.A.R.V.I.S.
Gère la synthèse vocale avec Tortoise TTS et Windows TTS
"""

import os
import sys
import logging
import pygame
import pyttsx3
import torch
from pathlib import Path
import json
import numpy as np
from io import BytesIO

# Import Tortoise TTS
try:
    from tortoise.api import TextToSpeech
    from tortoise.utils.audio import load_voice
    TORTOISE_AVAILABLE = True
except ImportError:
    TORTOISE_AVAILABLE = False
    logging.warning("Tortoise TTS non disponible. Utilisation de Windows TTS uniquement.")

class VoiceManager:
    def __init__(self, config):
        """Initialisation du gestionnaire vocal"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialisation pygame pour la lecture audio
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Initialisation Windows TTS
        self.windows_tts = pyttsx3.init()
        self.setup_windows_voice()
        
        # Initialisation Tortoise TTS
        self.tortoise_tts = None
        self.william_voice = None
        if TORTOISE_AVAILABLE:
            self.setup_tortoise_tts()
        
        self.logger.info("VoiceManager initialisé")
    
    def setup_windows_voice(self):
        """Configuration de la voix Windows"""
        voices = self.windows_tts.getProperty('voices')
        
        # Rechercher une voix française (priorité aux voix masculines)
        french_voice = None
        for voice in voices:
            voice_name = voice.name.lower()
            voice_id = voice.id.lower()
            
            # Vérifier si c'est une voix française
            if any(keyword in voice_name or keyword in voice_id 
                   for keyword in ['french', 'fr', 'français', 'francais']):
                french_voice = voice.id
                # Priorité aux voix masculines
                if any(keyword in voice_name 
                       for keyword in ['male', 'homme', 'man', 'david', 'guillaume']):
                    break
        
        if french_voice:
            self.windows_tts.setProperty('voice', french_voice)
            self.logger.info(f"Voix française configurée: {french_voice}")
        else:
            self.logger.warning("Aucune voix française trouvée, utilisation de la voix par défaut")
        
        # Configuration de la vitesse et du volume
        self.windows_tts.setProperty('rate', 180)  # Vitesse de parole
        self.windows_tts.setProperty('volume', 0.9)  # Volume
    
    def setup_tortoise_tts(self):
        """Configuration de Tortoise TTS avec la voix William"""
        try:
            self.tortoise_tts = TextToSpeech()
            
            # Chemin vers la voix William
            william_path = Path(self.config["voice"]["william_voice_path"])
            
            if william_path.exists():
                self.william_voice = load_voice("william", [str(william_path)])
                self.logger.info("Voix William chargée avec succès")
            else:
                self.logger.warning(f"Voix William non trouvée à: {william_path}")
                self.create_default_william_voice()
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'initialisation de Tortoise TTS: {e}")
            TORTOISE_AVAILABLE = False
    
    def create_default_william_voice(self):
        """Créer une voix William par défaut si elle n'existe pas"""
        william_dir = Path(self.config["voice"]["william_voice_path"])
        william_dir.mkdir(parents=True, exist_ok=True)
        
        # Créer un fichier de configuration pour la voix
        voice_config = {
            "name": "William",
            "language": "fr",
            "gender": "male",
            "created": "2025-01-11",
            "description": "Voix masculine française pour J.A.R.V.I.S."
        }
        
        with open(william_dir / "voice_config.json", 'w', encoding='utf-8') as f:
            json.dump(voice_config, f, indent=2, ensure_ascii=False)
        
        self.logger.info("Configuration voix William créée")
    
    def speak_with_tortoise(self, text):
        """Synthèse vocale avec Tortoise TTS (voix William)"""
        try:
            if not self.tortoise_tts or not self.william_voice:
                raise Exception("Tortoise TTS ou voix William non disponible")
            
            # Génération audio avec Tortoise
            gen = self.tortoise_tts.tts_with_preset(
                text, 
                voice_samples=self.william_voice, 
                preset='fast'
            )
            
            # Conversion en format pygame
            audio_data = gen.cpu().numpy()
            audio_data = (audio_data * 32767).astype(np.int16)
            
            # Lecture avec pygame
            sound = pygame.sndarray.make_sound(audio_data)
            sound.play()
            
            # Attendre la fin de la lecture
            while pygame.mixer.get_busy():
                pygame.time.wait(100)
                
        except Exception as e:
            self.logger.error(f"Erreur Tortoise TTS: {e}")
            # Fallback vers Windows TTS
            self.speak_with_windows(text)
    
    def speak_with_windows(self, text):
        """Synthèse vocale avec Windows TTS"""
        try:
            self.windows_tts.say(text)
            self.windows_tts.runAndWait()
        except Exception as e:
            self.logger.error(f"Erreur Windows TTS: {e}")
    
    def speak(self, text, voice="William"):
        """Interface principale pour la synthèse vocale"""
        if not text.strip():
            return
        
        self.logger.info(f"Synthèse vocale ({voice}): {text}")
        
        try:
            # Toujours utiliser Windows TTS en priorité car plus stable
            use_windows = (
                voice == "Windows" or 
                not TORTOISE_AVAILABLE or 
                not self.william_voice or
                self.config.get("voice", {}).get("fallback_to_windows", True)
            )
            
            if use_windows:
                self.speak_with_windows(text)
            else:
                # Tentative avec Tortoise, fallback vers Windows
                try:
                    self.speak_with_tortoise(text)
                except Exception as e:
                    self.logger.warning(f"Tortoise TTS échoué, fallback Windows: {e}")
                    self.speak_with_windows(text)
                    
        except Exception as e:
            self.logger.error(f"Erreur synthèse vocale: {e}")
            # Dernière chance avec Windows TTS basique
            try:
                self.speak_with_windows(text)
            except Exception as final_e:
                self.logger.error(f"Impossible de synthétiser la voix: {final_e}")
                print(f"🔊 [VOICE FAILED] {text}")
    
    def get_available_voices(self):
        """Obtenir la liste des voix disponibles"""
        voices = {"Windows": True}
        
        if TORTOISE_AVAILABLE and self.william_voice:
            voices["William"] = True
        else:
            voices["William"] = False
            
        return voices
    
    def test_voice(self, voice_name):
        """Tester une voix"""
        test_text = "Test de la voix. J.A.R.V.I.S. opérationnel."
        self.speak(test_text, voice_name)
        
    def cleanup(self):
        """Nettoyage des ressources"""
        try:
            pygame.mixer.quit()
        except:
            pass
        
        try:
            if self.windows_tts:
                self.windows_tts.stop()
        except:
            pass