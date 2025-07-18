#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module ElevenLabs pour J.A.R.V.I.S.
Alternative moderne à Tortoise TTS
"""

import requests
import json
import logging
import pygame
import io
from pathlib import Path

class ElevenLabsClient:
    """Client pour l'API ElevenLabs TTS"""
    
    def __init__(self, api_key, voice_id="9BWtsMINqrJLrRacOk9x"):  # Aria par défaut
        """
        Initialise le client ElevenLabs
        
        Args:
            api_key (str): Clé API ElevenLabs
            voice_id (str): ID de la voix (défaut: Aria)
        """
        self.api_key = api_key
        self.voice_id = voice_id
        self.base_url = "https://api.elevenlabs.io/v1"
        self.logger = logging.getLogger(__name__)
        
        # Configuration par défaut
        self.model = "eleven_multilingual_v2"  # Support français
        self.settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
        
        # Initialiser pygame pour l'audio
        try:
            pygame.mixer.init()
            self.audio_available = True
        except Exception as e:
            self.logger.warning(f"Pygame audio non disponible: {e}")
            self.audio_available = False
    
    def get_voices(self):
        """Récupère la liste des voix disponibles"""
        try:
            headers = {"xi-api-key": self.api_key}
            response = requests.get(f"{self.base_url}/voices", headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Erreur récupération voix: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des voix: {e}")
            return None
    
    def synthesize_speech(self, text, voice_id=None, model=None):
        """
        Synthétise le texte en audio
        
        Args:
            text (str): Texte à synthétiser
            voice_id (str): ID de la voix (optionnel)
            model (str): Modèle à utiliser (optionnel)
            
        Returns:
            bytes: Données audio MP3 ou None si erreur
        """
        if not voice_id:
            voice_id = self.voice_id
        if not model:
            model = self.model
            
        try:
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": model,
                "voice_settings": self.settings
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                return response.content
            else:
                self.logger.error(f"Erreur synthèse: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la synthèse: {e}")
            return None
    
    def speak(self, text, voice_id=None):
        """
        Synthétise et joue le texte
        
        Args:
            text (str): Texte à dire
            voice_id (str): ID de la voix (optionnel)
            
        Returns:
            bool: True si succès, False sinon
        """
        if not self.audio_available:
            self.logger.error("Audio non disponible")
            return False
            
        audio_data = self.synthesize_speech(text, voice_id)
        if not audio_data:
            return False
            
        try:
            # Créer un objet BytesIO pour pygame
            audio_buffer = io.BytesIO(audio_data)
            
            # Jouer l'audio
            pygame.mixer.music.load(audio_buffer)
            pygame.mixer.music.play()
            
            # Attendre la fin de la lecture
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la lecture audio: {e}")
            return False
    
    def save_audio(self, text, output_path, voice_id=None):
        """
        Synthétise et sauvegarde l'audio
        
        Args:
            text (str): Texte à synthétiser
            output_path (str): Chemin de sauvegarde
            voice_id (str): ID de la voix (optionnel)
            
        Returns:
            bool: True si succès, False sinon
        """
        audio_data = self.synthesize_speech(text, voice_id)
        if not audio_data:
            return False
            
        try:
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            return True
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde audio: {e}")
            return False
    
    def test_connection(self):
        """Teste la connexion à l'API"""
        try:
            voices = self.get_voices()
            if voices:
                self.logger.info("Connexion ElevenLabs réussie")
                return True
            else:
                self.logger.error("Échec test connexion ElevenLabs")
                return False
        except Exception as e:
            self.logger.error(f"Erreur test connexion: {e}")
            return False

# Voix françaises recommandées pour JARVIS
FRENCH_VOICES = {
    "masculine": {
        "Callum": "N2lVS1w4EtoT3dr4eOWO",
        "Liam": "TX3LPaxmHKxFdv7VOQHJ", 
        "George": "JBFqnCBsd6RMkjVDRZzb"
    },
    "feminine": {
        "Aria": "9BWtsMINqrJLrRacOk9x",
        "Sarah": "EXAVITQu4vr4xnSDxMaL",
        "Charlotte": "XB0fDUnXU5powFXDhCwa"
    }
}

def get_recommended_voice(gender="masculine"):
    """Retourne une voix recommandée pour JARVIS"""
    if gender == "masculine":
        return FRENCH_VOICES["masculine"]["Callum"]  # Voix masculine claire
    else:
        return FRENCH_VOICES["feminine"]["Aria"]     # Voix féminine par défaut