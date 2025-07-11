#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de surveillance d'écran pour J.A.R.V.I.S.
OCR et analyse du contenu affiché
"""

import logging
import threading
import time
from datetime import datetime
import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageGrab
import pyautogui
from pathlib import Path

class ScreenMonitor:
    def __init__(self, config):
        """Initialisation du moniteur d'écran"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Configuration OCR
        self.ocr_enabled = config["screen"]["ocr_enabled"]
        self.monitoring_interval = config["screen"]["monitoring_interval"]
        
        # État du monitoring
        self.is_monitoring = False
        self.current_screen_text = ""
        self.last_screenshot = None
        self.monitor_thread = None
        
        # Configuration Tesseract
        self.setup_tesseract()
        
        # Historique des captures
        self.screenshot_history = []
        self.max_history = 10
        
        self.logger.info("ScreenMonitor initialisé")
    
    def setup_tesseract(self):
        """Configuration de Tesseract OCR"""
        try:
            # Tenter de configurer le chemin Tesseract (Windows)
            possible_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                "tesseract"  # Si dans PATH
            ]
            
            for path in possible_paths:
                try:
                    pytesseract.pytesseract.tesseract_cmd = path
                    # Test simple
                    test_image = Image.new('RGB', (100, 50), color='white')
                    pytesseract.image_to_string(test_image)
                    self.logger.info(f"Tesseract configuré: {path}")
                    return
                except:
                    continue
            
            self.logger.warning("Tesseract non trouvé. OCR désactivé.")
            self.ocr_enabled = False
            
        except Exception as e:
            self.logger.error(f"Erreur configuration Tesseract: {e}")
            self.ocr_enabled = False
    
    def capture_screen(self):
        """Capturer l'écran complet"""
        try:
            screenshot = ImageGrab.grab()
            
            # Ajouter timestamp
            screenshot_data = {
                "timestamp": datetime.now(),
                "image": screenshot,
                "size": screenshot.size
            }
            
            # Ajouter à l'historique
            self.screenshot_history.append(screenshot_data)
            if len(self.screenshot_history) > self.max_history:
                self.screenshot_history.pop(0)
            
            self.last_screenshot = screenshot
            return screenshot
            
        except Exception as e:
            self.logger.error(f"Erreur capture d'écran: {e}")
            return None
    
    def extract_text_from_image(self, image):
        """Extraire le texte d'une image avec OCR"""
        if not self.ocr_enabled:
            return ""
        
        try:
            # Configuration OCR pour le français
            config = r'--oem 3 --psm 6 -l fra'
            
            # Convertir PIL en format compatible
            if hasattr(image, 'convert'):
                image = image.convert('RGB')
            
            # Extraction du texte
            text = pytesseract.image_to_string(image, config=config)
            
            # Nettoyer le texte
            cleaned_text = self.clean_extracted_text(text)
            
            return cleaned_text
            
        except Exception as e:
            self.logger.error(f"Erreur OCR: {e}")
            return ""
    
    def clean_extracted_text(self, text):
        """Nettoyer le texte extrait par OCR"""
        if not text:
            return ""
        
        # Supprimer les caractères indésirables
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Ignorer les lignes trop courtes ou vides
            if len(line) > 2:
                cleaned_lines.append(line)
        
        # Rejoindre les lignes
        cleaned_text = ' '.join(cleaned_lines)
        
        # Limiter la longueur
        if len(cleaned_text) > 500:
            cleaned_text = cleaned_text[:500] + "..."
        
        return cleaned_text
    
    def analyze_screen(self):
        """Analyser le contenu actuel de l'écran"""
        screenshot = self.capture_screen()
        if not screenshot:
            return "Impossible de capturer l'écran"
        
        # Extraction du texte
        extracted_text = self.extract_text_from_image(screenshot)
        
        # Analyse basique du contenu
        analysis = self.analyze_content(extracted_text, screenshot)
        
        return analysis
    
    def analyze_content(self, text, image):
        """Analyser le contenu de l'écran"""
        analysis_parts = []
        
        if text.strip():
            # Détection de types de contenu
            text_lower = text.lower()
            
            if any(word in text_lower for word in ['error', 'erreur', 'exception']):
                analysis_parts.append("Une erreur semble être affichée")
            
            if any(word in text_lower for word in ['menu', 'fichier', 'édition']):
                analysis_parts.append("Interface d'application avec menus")
            
            if any(word in text_lower for word in ['vitesse', 'rpm', 'gear']):
                analysis_parts.append("Interface de jeu de course détectée")
            
            if any(word in text_lower for word in ['altitude', 'heading', 'speed']):
                analysis_parts.append("Interface de simulation de vol détectée")
            
            # Ajouter le texte extrait
            if len(text) > 50:
                analysis_parts.append(f"Texte principal: {text[:100]}...")
            else:
                analysis_parts.append(f"Texte visible: {text}")
        else:
            analysis_parts.append("Principalement du contenu graphique")
        
        # Analyser la taille de l'image
        if image:
            width, height = image.size
            analysis_parts.append(f"Résolution: {width}x{height}")
        
        return " | ".join(analysis_parts) if analysis_parts else "Écran analysé"
    
    def start_monitoring(self):
        """Démarrer la surveillance continue"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info("Surveillance d'écran démarrée")
    
    def stop_monitoring(self):
        """Arrêter la surveillance"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        self.logger.info("Surveillance d'écran arrêtée")
    
    def _monitor_loop(self):
        """Boucle de surveillance en arrière-plan"""
        while self.is_monitoring:
            try:
                self.update_screen_data()
                time.sleep(self.monitoring_interval)
            except Exception as e:
                self.logger.error(f"Erreur dans la boucle de surveillance: {e}")
                time.sleep(5)
    
    def update_screen_data(self):
        """Mettre à jour les données d'écran"""
        screenshot = self.capture_screen()
        if screenshot:
            self.current_screen_text = self.extract_text_from_image(screenshot)
    
    def get_current_screen_text(self):
        """Obtenir le texte actuel de l'écran"""
        return self.current_screen_text
    
    def get_screen_region(self, x, y, width, height):
        """Capturer une région spécifique de l'écran"""
        try:
            region = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            return self.extract_text_from_image(region)
        except Exception as e:
            self.logger.error(f"Erreur capture région: {e}")
            return ""
    
    def find_text_on_screen(self, search_text):
        """Rechercher un texte spécifique sur l'écran"""
        current_text = self.get_current_screen_text()
        return search_text.lower() in current_text.lower()
    
    def save_screenshot(self, filename=None):
        """Sauvegarder une capture d'écran"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True)
        
        screenshot = self.capture_screen()
        if screenshot:
            filepath = screenshot_dir / filename
            screenshot.save(filepath)
            self.logger.info(f"Capture sauvegardée: {filepath}")
            return str(filepath)
        
        return None
    
    def get_status(self):
        """Obtenir le statut du moniteur"""
        return {
            "monitoring": self.is_monitoring,
            "ocr_enabled": self.ocr_enabled,
            "last_screenshot_time": self.screenshot_history[-1]["timestamp"] if self.screenshot_history else None,
            "current_text_length": len(self.current_screen_text),
            "history_count": len(self.screenshot_history)
        }