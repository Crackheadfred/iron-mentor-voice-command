#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'aide cockpit DCS F/A-18 pour J.A.R.V.I.S.
Assistant pour DCS World F/A-18C Hornet
"""

import logging
import json
import psutil
import time
import threading
from datetime import datetime
from pathlib import Path

class DCSCockpit:
    def __init__(self, config):
        """Initialisation de l'assistant cockpit DCS"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Configuration
        self.dcs_enabled = config["dcs"]["enabled"]
        self.aircraft = config["dcs"]["aircraft"]
        
        # État du module
        self.is_active = False
        self.dcs_running = False
        self.current_phase = "parked"  # parked, startup, taxi, takeoff, flight, landing
        
        # Base de connaissances F/A-18C
        self.knowledge_base = self.load_fa18_knowledge()
        
        # Procédures
        self.procedures = {
            "startup": [
                "1. Batterie ON",
                "2. Générateurs ON",
                "3. Moteurs - démarrage séquentiel",
                "4. Avionique - initialisation",
                "5. Navigation - alignement INS",
                "6. Systèmes d'armes - test",
                "7. Contrôles de vol - vérification"
            ],
            "takeoff": [
                "1. Volets - UP",
                "2. Compensateur - neutre",
                "3. Moteurs - poussée militaire",
                "4. Vitesse rotation - 140 knots",
                "5. Angle de montée - 15°",
                "6. Train d'atterrissage - UP"
            ],
            "landing": [
                "1. Vitesse d'approche - 135 knots",
                "2. Volets - DOWN",
                "3. Train d'atterrissage - DOWN",
                "4. Crosse d'appontage - DOWN (si porte-avions)",
                "5. Gestion de la puissance",
                "6. Angle d'approche - 3.5°"
            ]
        }
        
        # Surveillance DCS
        if self.dcs_enabled:
            self.start_dcs_monitoring()
        
        self.logger.info("DCSCockpit initialisé")
    
    def load_fa18_knowledge(self):
        """Charger la base de connaissances F/A-18C"""
        knowledge = {
            "systemes": {
                "radar": {
                    "activation": "RDR PWR switch ON, puis sélecteur de mode",
                    "modes": {
                        "RWS": "Real While Scan - balayage de recherche",
                        "TWS": "Track While Scan - suivi multiple",
                        "STT": "Single Target Track - verrouillage unique",
                        "LTWS": "Long Track While Scan"
                    },
                    "commandes": {
                        "elevation": "Crank de l'antenne",
                        "azimuth": "Sélecteur d'azimuth",
                        "range": "Bouton de portée"
                    }
                },
                "rwr": {
                    "activation": "RWR switch ON sur panneau sensor",
                    "symboles": {
                        "triangle": "Radar de chasse",
                        "chapeau": "Radar SAM",
                        "losange": "Radar naval"
                    }
                },
                "armement": {
                    "air_air": {
                        "AIM-120": "Missile moyenne portée actif",
                        "AIM-9": "Missile courte portée infrarouge",
                        "AIM-7": "Missile moyenne portée semi-actif"
                    },
                    "air_sol": {
                        "AGM-65": "Missile Maverick",
                        "AGM-88": "Missile anti-radiation HARM",
                        "bombes": "Mk-82, Mk-83, Mk-84, GBU series"
                    }
                }
            },
            "procedures_urgence": {
                "engine_fire": [
                    "Throttle - IDLE",
                    "Fire switch - PUSH",
                    "Engine master - OFF",
                    "Atterrissage d'urgence"
                ],
                "hydraulic_failure": [
                    "Système de secours - ON",
                    "Contrôles - test",
                    "Atterrissage précautionneux"
                ]
            }
        }
        return knowledge
    
    def start_dcs_monitoring(self):
        """Démarrer la surveillance de DCS World"""
        def monitor():
            while True:
                self.check_dcs_status()
                time.sleep(10)
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def check_dcs_status(self):
        """Vérifier si DCS World est en cours d'exécution"""
        try:
            dcs_processes = [
                "DCS.exe",
                "DCS_updater.exe",
                "DCSWorld.exe"
            ]
            
            running = False
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] in dcs_processes:
                    running = True
                    break
            
            was_running = self.dcs_running
            self.dcs_running = running
            
            if running and not was_running:
                self.logger.info("DCS World détecté")
                if self.is_active:
                    return "DCS World détecté. Module F/A-18 prêt."
            elif not running and was_running:
                self.logger.info("DCS World fermé")
                
        except Exception as e:
            self.logger.error(f"Erreur surveillance DCS: {e}")
    
    def activate(self):
        """Activer le module DCS F/A-18"""
        self.is_active = True
        self.logger.info("Module DCS F/A-18 activé")
        
        if self.dcs_running:
            return "Module F/A-18 activé. DCS World détecté. Je suis prêt à vous assister."
        else:
            return "Module F/A-18 activé. DCS World non détecté. Lancez DCS pour une assistance complète."
    
    def deactivate(self):
        """Désactiver le module"""
        self.is_active = False
        self.logger.info("Module DCS F/A-18 désactivé")
        return "Module F/A-18 désactivé."
    
    def handle_command(self, command):
        """Traiter une commande liée au F/A-18"""
        command_lower = command.lower()
        
        # Commandes de procédures
        if "startup" in command_lower or "démarrage" in command_lower:
            return self.get_startup_procedure()
        
        if "takeoff" in command_lower or "décollage" in command_lower:
            return self.get_takeoff_procedure()
        
        if "landing" in command_lower or "atterrissage" in command_lower:
            return self.get_landing_procedure()
        
        # Commandes systèmes
        if "radar" in command_lower:
            return self.explain_radar_system()
        
        if "rwr" in command_lower:
            return self.explain_rwr_system()
        
        if "armement" in command_lower or "armes" in command_lower:
            return self.explain_weapons()
        
        if "urgence" in command_lower or "emergency" in command_lower:
            return self.get_emergency_procedures()
        
        # Préparation générale
        if "prépare" in command_lower and "avion" in command_lower:
            return self.prepare_aircraft()
        
        # Commande générale
        return self.general_assistance(command)
    
    def get_startup_procedure(self):
        """Procédure de démarrage"""
        steps = self.procedures["startup"]
        response = "Procédure de démarrage F/A-18C:\n"
        response += "\n".join(steps)
        response += "\n\nVoulez-vous des détails sur une étape particulière?"
        return response
    
    def get_takeoff_procedure(self):
        """Procédure de décollage"""
        steps = self.procedures["takeoff"]
        response = "Procédure de décollage F/A-18C:\n"
        response += "\n".join(steps)
        return response
    
    def get_landing_procedure(self):
        """Procédure d'atterrissage"""
        steps = self.procedures["landing"]
        response = "Procédure d'atterrissage F/A-18C:\n"
        response += "\n".join(steps)
        return response
    
    def explain_radar_system(self):
        """Expliquer le système radar"""
        radar_info = self.knowledge_base["systemes"]["radar"]
        
        response = "Système radar AN/APG-73:\n"
        response += f"Activation: {radar_info['activation']}\n\n"
        response += "Modes principaux:\n"
        
        for mode, description in radar_info["modes"].items():
            response += f"• {mode}: {description}\n"
        
        response += "\nCommandes principales sur le stick et les panneaux MFD."
        return response
    
    def explain_rwr_system(self):
        """Expliquer le RWR"""
        rwr_info = self.knowledge_base["systemes"]["rwr"]
        
        response = "Récepteur d'alerte radar (RWR):\n"
        response += f"Activation: {rwr_info['activation']}\n\n"
        response += "Symboles principaux:\n"
        
        for symbole, description in rwr_info["symboles"].items():
            response += f"• {symbole}: {description}\n"
        
        return response
    
    def explain_weapons(self):
        """Expliquer les systèmes d'armement"""
        weapons = self.knowledge_base["systemes"]["armement"]
        
        response = "Systèmes d'armement F/A-18C:\n\n"
        response += "Air-Air:\n"
        for weapon, desc in weapons["air_air"].items():
            response += f"• {weapon}: {desc}\n"
        
        response += "\nAir-Sol:\n"
        for weapon, desc in weapons["air_sol"].items():
            response += f"• {weapon}: {desc}\n"
        
        return response
    
    def get_emergency_procedures(self):
        """Procédures d'urgence"""
        emergencies = self.knowledge_base["procedures_urgence"]
        
        response = "Procédures d'urgence principales:\n\n"
        
        for emergency, steps in emergencies.items():
            response += f"{emergency.replace('_', ' ').title()}:\n"
            for step in steps:
                response += f"• {step}\n"
            response += "\n"
        
        return response
    
    def prepare_aircraft(self):
        """Préparer l'avion pour le décollage"""
        response = "Préparation de l'appareil pour le décollage:\n\n"
        response += "1. Effectuez la procédure de démarrage complète\n"
        response += "2. Vérifiez tous les systèmes (radar, RWR, contre-mesures)\n"
        response += "3. Configurez l'armement selon la mission\n"
        response += "4. Programmez les waypoints de navigation\n"
        response += "5. Test des systèmes de communication\n"
        response += "6. Vérification des surfaces de contrôle\n"
        response += "7. Configuration des contre-mesures (chaff/flare)\n\n"
        response += "Tous les systèmes verts, monsieur. Prêt pour le décollage."
        
        return response
    
    def general_assistance(self, command):
        """Assistance générale"""
        command_lower = command.lower()
        
        # Recherche de mots-clés dans la base de connaissances
        if "switch" in command_lower or "bouton" in command_lower:
            return "Spécifiez le système concerné pour une aide précise sur les commandes."
        
        if "mfd" in command_lower:
            return "Les écrans multifonctions (MFD) affichent les informations systèmes. Utilisez les boutons autour de l'écran pour naviguer."
        
        if "hud" in command_lower:
            return "Le HUD affiche les informations de vol essentielles: vitesse, altitude, cap, et symboles de visée."
        
        if "navigation" in command_lower:
            return "Système de navigation INS. Alignement requis avant le décollage. Programmation des waypoints via les MFD."
        
        # Réponse par défaut
        return "Je peux vous aider avec le F/A-18C. Demandez-moi des informations sur les systèmes, procédures, ou urgences."
    
    def get_system_status(self):
        """Obtenir le statut des systèmes"""
        # Simulation du statut des systèmes
        systems_status = {
            "Moteurs": "NORMAL",
            "Hydraulique": "NORMAL", 
            "Électrique": "NORMAL",
            "Radar": "STANDBY",
            "RWR": "ACTIVE",
            "Navigation": "ALIGNED",
            "Communication": "ACTIVE"
        }
        
        response = "État des systèmes F/A-18C:\n"
        for system, status in systems_status.items():
            response += f"• {system}: {status}\n"
        
        return response
    
    def get_checklist(self, phase):
        """Obtenir une checklist pour une phase de vol"""
        checklists = {
            "preflight": [
                "Inspection visuelle externe",
                "Vérification du carburant",
                "Test des surfaces de contrôle",
                "Vérification de l'armement",
                "Check des pneus et freins"
            ],
            "postflight": [
                "Arrêt des moteurs",
                "Systèmes électriques OFF",
                "Sécurisation de l'armement",
                "Rapport de vol",
                "Inspection post-vol"
            ]
        }
        
        if phase in checklists:
            response = f"Checklist {phase}:\n"
            for i, item in enumerate(checklists[phase], 1):
                response += f"{i}. {item}\n"
            return response
        else:
            return "Phase non reconnue. Phases disponibles: preflight, postflight."
    
    def get_status(self):
        """Obtenir le statut du module"""
        return {
            "active": self.is_active,
            "dcs_running": self.dcs_running,
            "aircraft": self.aircraft,
            "current_phase": self.current_phase,
            "enabled": self.dcs_enabled
        }