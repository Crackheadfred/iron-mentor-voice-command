#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module mécanicien virtuel pour J.A.R.V.I.S.
Interface avec SimHub et analyse de télémétrie
"""

import logging
import json
import requests
import socket
import threading
import time
from datetime import datetime
from pathlib import Path

class SimHubMechanic:
    def __init__(self, config):
        """Initialisation du mécanicien virtuel"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Configuration SimHub
        self.simhub_enabled = config["simhub"]["enabled"]
        self.simhub_port = config["simhub"]["port"]
        self.simhub_host = "localhost"
        
        # État de connexion
        self.connected = False
        self.telemetry_data = {}
        self.last_update = None
        
        # Données de performance
        self.lap_times = []
        self.sector_times = []
        self.tire_data = {}
        self.setup_recommendations = []
        
        # Configuration des jeux supportés
        self.supported_games = [
            "Assetto Corsa",
            "Assetto Corsa EVO", 
            "Forza Motorsport 8",
            "Automobilista 2",
            "Le Mans Ultimate",
            "F1 24", "F1 23", "F1 22",
            "Project CARS 2",
            "RENNSPORT",
            "RaceRoom Racing Experience",
            "KartKraft"
        ]
        
        # Seuils d'analyse
        self.analysis_thresholds = {
            "tire_temp_optimal": {"front": (85, 95), "rear": (85, 95)},
            "tire_pressure_optimal": {"front": (24, 26), "rear": (23, 25)},
            "fuel_consumption_warning": 0.1,  # 10% restant
            "damage_threshold": 0.05  # 5% de dégâts
        }
        
        self.logger.info("SimHubMechanic initialisé")
        
        if self.simhub_enabled:
            self.start_connection_monitoring()
    
    def start_connection_monitoring(self):
        """Démarrer la surveillance de connexion SimHub"""
        def monitor():
            while True:
                self.check_simhub_connection()
                time.sleep(5)
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def check_simhub_connection(self):
        """Vérifier la connexion à SimHub"""
        try:
            # Tenter de se connecter au port SimHub
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.simhub_host, self.simhub_port))
            sock.close()
            
            was_connected = self.connected
            self.connected = (result == 0)
            
            if self.connected and not was_connected:
                self.logger.info("Connexion SimHub établie")
            elif not self.connected and was_connected:
                self.logger.warning("Connexion SimHub perdue")
                
        except Exception as e:
            self.connected = False
    
    def is_connected(self):
        """Vérifier si SimHub est connecté"""
        return self.connected
    
    def get_telemetry_data(self):
        """Récupérer les données de télémétrie depuis SimHub"""
        if not self.connected:
            return None
        
        try:
            # SimHub expose généralement les données via HTTP ou UDP
            # Ici on simule une connexion HTTP
            response = requests.get(
                f"http://{self.simhub_host}:{self.simhub_port}/api/telemetry",
                timeout=2
            )
            
            if response.status_code == 200:
                data = response.json()
                self.telemetry_data = data
                self.last_update = datetime.now()
                return data
                
        except requests.exceptions.ConnectionError:
            self.connected = False
        except Exception as e:
            self.logger.error(f"Erreur récupération télémétrie: {e}")
        
        return None
    
    def update_telemetry(self):
        """Mettre à jour les données de télémétrie"""
        data = self.get_telemetry_data()
        if data:
            self.analyze_performance(data)
    
    def analyze_performance(self, data):
        """Analyser les performances et générer des recommandations"""
        try:
            recommendations = []
            
            # Analyse des pneus
            tire_analysis = self.analyze_tires(data)
            if tire_analysis:
                recommendations.extend(tire_analysis)
            
            # Analyse de la consommation
            fuel_analysis = self.analyze_fuel(data)
            if fuel_analysis:
                recommendations.extend(fuel_analysis)
            
            # Analyse des temps au tour
            lap_analysis = self.analyze_lap_times(data)
            if lap_analysis:
                recommendations.extend(lap_analysis)
            
            # Analyse de l'aérodynamique
            aero_analysis = self.analyze_aerodynamics(data)
            if aero_analysis:
                recommendations.extend(aero_analysis)
            
            self.setup_recommendations = recommendations
            
        except Exception as e:
            self.logger.error(f"Erreur analyse performance: {e}")
    
    def analyze_tires(self, data):
        """Analyser l'état des pneus"""
        recommendations = []
        
        try:
            # Températures des pneus
            front_temp = data.get("tire_temp_front_avg", 0)
            rear_temp = data.get("tire_temp_rear_avg", 0)
            
            optimal_front = self.analysis_thresholds["tire_temp_optimal"]["front"]
            optimal_rear = self.analysis_thresholds["tire_temp_optimal"]["rear"]
            
            if front_temp < optimal_front[0]:
                recommendations.append("Pneus avant trop froids. Augmentez la pression ou changez les réglages de suspension.")
            elif front_temp > optimal_front[1]:
                recommendations.append("Pneus avant en surchauffe. Réduisez la pression ou ajustez l'aérodynamique.")
            
            if rear_temp < optimal_rear[0]:
                recommendations.append("Pneus arrière trop froids. Vérifiez la géométrie et la pression.")
            elif rear_temp > optimal_rear[1]:
                recommendations.append("Pneus arrière en surchauffe. Réduisez l'agressivité ou ajustez la suspension.")
            
            # Pression des pneus
            front_pressure = data.get("tire_pressure_front", 0)
            rear_pressure = data.get("tire_pressure_rear", 0)
            
            if front_pressure < 20:
                recommendations.append("Pression pneus avant trop faible.")
            elif front_pressure > 30:
                recommendations.append("Pression pneus avant trop élevée.")
            
        except Exception as e:
            self.logger.error(f"Erreur analyse pneus: {e}")
        
        return recommendations
    
    def analyze_fuel(self, data):
        """Analyser la consommation de carburant"""
        recommendations = []
        
        try:
            fuel_level = data.get("fuel_level", 1.0)
            fuel_consumption = data.get("fuel_consumption_per_lap", 0)
            laps_remaining = data.get("laps_remaining", 0)
            
            if fuel_level < self.analysis_thresholds["fuel_consumption_warning"]:
                recommendations.append("Niveau de carburant critique. Économisez le carburant.")
            
            if fuel_consumption > 0 and laps_remaining > 0:
                fuel_needed = fuel_consumption * laps_remaining
                if fuel_needed > fuel_level:
                    recommendations.append(f"Carburant insuffisant. Il vous faut {fuel_needed:.1f}L pour finir.")
                    
        except Exception as e:
            self.logger.error(f"Erreur analyse carburant: {e}")
        
        return recommendations
    
    def analyze_lap_times(self, data):
        """Analyser les temps au tour"""
        recommendations = []
        
        try:
            current_lap_time = data.get("current_lap_time", 0)
            best_lap_time = data.get("best_lap_time", 0)
            
            if current_lap_time > 0:
                self.lap_times.append(current_lap_time)
                
                # Garder seulement les 10 derniers tours
                if len(self.lap_times) > 10:
                    self.lap_times.pop(0)
                
                # Analyser la consistance
                if len(self.lap_times) >= 3:
                    avg_time = sum(self.lap_times) / len(self.lap_times)
                    variation = max(self.lap_times) - min(self.lap_times)
                    
                    if variation > 2.0:  # Plus de 2 secondes d'écart
                        recommendations.append("Manque de consistance. Concentrez-vous sur la régularité.")
                    
                    if current_lap_time > avg_time + 1.0:
                        recommendations.append("Tour plus lent que la moyenne. Vérifiez votre ligne de course.")
                        
        except Exception as e:
            self.logger.error(f"Erreur analyse temps au tour: {e}")
        
        return recommendations
    
    def analyze_aerodynamics(self, data):
        """Analyser les réglages aérodynamiques"""
        recommendations = []
        
        try:
            downforce_front = data.get("downforce_front", 0)
            downforce_rear = data.get("downforce_rear", 0)
            top_speed = data.get("top_speed_kmh", 0)
            
            # Analyse basée sur le type de circuit
            circuit_type = self.detect_circuit_type(data)
            
            if circuit_type == "high_speed":
                if downforce_front > 5 or downforce_rear > 15:
                    recommendations.append("Circuit rapide détecté. Réduisez l'appui aérodynamique.")
            elif circuit_type == "technical":
                if downforce_front < 8 or downforce_rear < 12:
                    recommendations.append("Circuit technique détecté. Augmentez l'appui aérodynamique.")
                    
        except Exception as e:
            self.logger.error(f"Erreur analyse aérodynamique: {e}")
        
        return recommendations
    
    def detect_circuit_type(self, data):
        """Détecter le type de circuit"""
        try:
            avg_speed = data.get("average_speed_kmh", 0)
            max_speed = data.get("top_speed_kmh", 0)
            
            if max_speed > 300 or avg_speed > 200:
                return "high_speed"
            elif max_speed < 200 or avg_speed < 120:
                return "technical"
            else:
                return "mixed"
                
        except:
            return "unknown"
    
    def get_telemetry_advice(self):
        """Obtenir des conseils basés sur la télémétrie actuelle"""
        if not self.connected:
            return "SimHub non connecté. Lancez votre jeu de course et SimHub."
        
        if not self.telemetry_data:
            return "Aucune donnée de télémétrie disponible."
        
        if not self.setup_recommendations:
            return "Tous les paramètres semblent optimaux, monsieur."
        
        # Limiter à 3 recommandations principales
        top_recommendations = self.setup_recommendations[:3]
        advice = "Recommandations mécaniques: " + " | ".join(top_recommendations)
        
        return advice
    
    def get_current_telemetry(self):
        """Obtenir les données de télémétrie actuelles"""
        return self.telemetry_data
    
    def get_performance_summary(self):
        """Obtenir un résumé des performances"""
        if not self.telemetry_data:
            return "Aucune donnée disponible"
        
        try:
            summary_parts = []
            
            # Vitesse actuelle
            speed = self.telemetry_data.get("speed_kmh", 0)
            if speed > 0:
                summary_parts.append(f"Vitesse: {speed:.0f} km/h")
            
            # Régime moteur
            rpm = self.telemetry_data.get("rpm", 0)
            if rpm > 0:
                summary_parts.append(f"Régime: {rpm:.0f} RPM")
            
            # Rapport de vitesse
            gear = self.telemetry_data.get("gear", 0)
            if gear > 0:
                summary_parts.append(f"Rapport: {gear}")
            
            # Position
            position = self.telemetry_data.get("position", 0)
            if position > 0:
                summary_parts.append(f"Position: {position}")
            
            return " | ".join(summary_parts) if summary_parts else "Données limitées"
            
        except Exception as e:
            self.logger.error(f"Erreur résumé performance: {e}")
            return "Erreur lors de l'analyse"
    
    def save_telemetry_log(self):
        """Sauvegarder les données de télémétrie"""
        if not self.telemetry_data:
            return False
        
        try:
            logs_dir = Path("logs/telemetry")
            logs_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = logs_dir / f"telemetry_{timestamp}.json"
            
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "telemetry": self.telemetry_data,
                "recommendations": self.setup_recommendations,
                "lap_times": self.lap_times
            }
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Télémétrie sauvegardée: {log_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde télémétrie: {e}")
            return False
    
    def get_status(self):
        """Obtenir le statut du mécanicien virtuel"""
        return {
            "connected": self.connected,
            "simhub_enabled": self.simhub_enabled,
            "last_update": self.last_update.isoformat() if self.last_update else None,
            "recommendations_count": len(self.setup_recommendations),
            "lap_times_recorded": len(self.lap_times),
            "supported_games": self.supported_games
        }