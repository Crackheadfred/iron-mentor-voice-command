#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de mémoire pour J.A.R.V.I.S.
Stockage local des interactions et contexte
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import threading

class MemoryManager:
    def __init__(self):
        """Initialisation du gestionnaire de mémoire"""
        self.logger = logging.getLogger(__name__)
        
        # Configuration des chemins
        self.memory_dir = Path("memory")
        self.memory_dir.mkdir(exist_ok=True)
        
        self.db_path = self.memory_dir / "jarvis_memory.db"
        self.json_backup_path = self.memory_dir / "interactions_backup.json"
        
        # Initialisation de la base de données
        self.init_database()
        
        # Cache en mémoire
        self.recent_interactions = []
        self.max_recent = 50
        
        # Verrou pour les accès concurrents
        self.lock = threading.Lock()
        
        self.logger.info("MemoryManager initialisé")
    
    def init_database(self):
        """Initialiser la base de données SQLite"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Table des interactions
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS interactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        speaker TEXT NOT NULL,
                        content TEXT NOT NULL,
                        context TEXT,
                        session_id TEXT
                    )
                ''')
                
                # Table des sessions
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sessions (
                        id TEXT PRIMARY KEY,
                        start_time TEXT NOT NULL,
                        end_time TEXT,
                        interaction_count INTEGER DEFAULT 0
                    )
                ''')
                
                # Table des préférences utilisateur
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                ''')
                
                # Index pour les recherches
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_interactions_timestamp 
                    ON interactions(timestamp)
                ''')
                
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_interactions_speaker 
                    ON interactions(speaker)
                ''')
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Erreur initialisation database: {e}")
    
    def add_interaction(self, speaker, content, context=None):
        """Ajouter une interaction à la mémoire"""
        with self.lock:
            try:
                timestamp = datetime.now().isoformat()
                session_id = self.get_current_session_id()
                
                # Ajouter à la base de données
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO interactions (timestamp, speaker, content, context, session_id)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (timestamp, speaker, content, json.dumps(context) if context else None, session_id))
                    conn.commit()
                
                # Ajouter au cache récent
                interaction = {
                    "timestamp": timestamp,
                    "speaker": speaker,
                    "content": content,
                    "context": context
                }
                
                self.recent_interactions.append(interaction)
                
                # Limiter le cache
                if len(self.recent_interactions) > self.max_recent:
                    self.recent_interactions.pop(0)
                
                # Sauvegarder périodiquement en JSON
                self.backup_to_json()
                
            except Exception as e:
                self.logger.error(f"Erreur ajout interaction: {e}")
    
    def get_recent_interactions(self, count=10):
        """Récupérer les interactions récentes"""
        with self.lock:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT timestamp, speaker, content, context
                        FROM interactions
                        ORDER BY timestamp DESC
                        LIMIT ?
                    ''', (count,))
                    
                    interactions = []
                    for row in cursor.fetchall():
                        interaction = {
                            "timestamp": row[0],
                            "speaker": row[1],
                            "content": row[2],
                            "context": json.loads(row[3]) if row[3] else None
                        }
                        interactions.append(interaction)
                    
                    return list(reversed(interactions))  # Ordre chronologique
                    
            except Exception as e:
                self.logger.error(f"Erreur récupération interactions: {e}")
                return self.recent_interactions[-count:] if self.recent_interactions else []
    
    def search_interactions(self, query, days_back=7, speaker=None):
        """Rechercher dans les interactions"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                sql = '''
                    SELECT timestamp, speaker, content, context
                    FROM interactions
                    WHERE timestamp >= ? AND content LIKE ?
                '''
                params = [cutoff_date, f'%{query}%']
                
                if speaker:
                    sql += ' AND speaker = ?'
                    params.append(speaker)
                
                sql += ' ORDER BY timestamp DESC LIMIT 20'
                
                cursor.execute(sql, params)
                
                results = []
                for row in cursor.fetchall():
                    result = {
                        "timestamp": row[0],
                        "speaker": row[1],
                        "content": row[2],
                        "context": json.loads(row[3]) if row[3] else None
                    }
                    results.append(result)
                
                return results
                
        except Exception as e:
            self.logger.error(f"Erreur recherche interactions: {e}")
            return []
    
    def get_current_session_id(self):
        """Obtenir l'ID de session actuel"""
        # Session basée sur la date (nouvelle session chaque jour)
        return datetime.now().strftime("%Y%m%d")
    
    def start_new_session(self):
        """Démarrer une nouvelle session"""
        try:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO sessions (id, start_time)
                    VALUES (?, ?)
                ''', (session_id, datetime.now().isoformat()))
                conn.commit()
            
            return session_id
            
        except Exception as e:
            self.logger.error(f"Erreur nouvelle session: {e}")
            return self.get_current_session_id()
    
    def get_conversation_context(self, messages_count=5):
        """Obtenir le contexte de conversation récent"""
        recent = self.get_recent_interactions(messages_count)
        
        context = {
            "recent_interactions": recent,
            "interaction_count": len(recent),
            "last_user_message": None,
            "last_jarvis_response": None
        }
        
        # Extraire les derniers messages
        for interaction in reversed(recent):
            if interaction["speaker"] == "user" and not context["last_user_message"]:
                context["last_user_message"] = interaction["content"]
            elif interaction["speaker"] == "jarvis" and not context["last_jarvis_response"]:
                context["last_jarvis_response"] = interaction["content"]
        
        return context
    
    def set_user_preference(self, key, value):
        """Définir une préférence utilisateur"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO user_preferences (key, value, updated_at)
                    VALUES (?, ?, ?)
                ''', (key, json.dumps(value), datetime.now().isoformat()))
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde préférence: {e}")
    
    def get_user_preference(self, key, default=None):
        """Récupérer une préférence utilisateur"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT value FROM user_preferences WHERE key = ?
                ''', (key,))
                
                row = cursor.fetchone()
                if row:
                    return json.loads(row[0])
                
        except Exception as e:
            self.logger.error(f"Erreur récupération préférence: {e}")
        
        return default
    
    def backup_to_json(self):
        """Sauvegarder les interactions en JSON"""
        try:
            # Sauvegarde uniquement si plus de 10 interactions depuis la dernière
            if len(self.recent_interactions) % 10 != 0:
                return
            
            recent_interactions = self.get_recent_interactions(100)
            
            backup_data = {
                "backup_timestamp": datetime.now().isoformat(),
                "interactions": recent_interactions
            }
            
            with open(self.json_backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde JSON: {e}")
    
    def restore_from_json(self):
        """Restaurer depuis la sauvegarde JSON"""
        try:
            if not self.json_backup_path.exists():
                return False
            
            with open(self.json_backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            interactions = backup_data.get("interactions", [])
            
            # Restaurer en base
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for interaction in interactions:
                    cursor.execute('''
                        INSERT OR IGNORE INTO interactions 
                        (timestamp, speaker, content, context, session_id)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        interaction["timestamp"],
                        interaction["speaker"], 
                        interaction["content"],
                        json.dumps(interaction.get("context")),
                        "restored"
                    ))
                
                conn.commit()
            
            self.logger.info(f"Restauré {len(interactions)} interactions depuis JSON")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur restauration JSON: {e}")
            return False
    
    def get_statistics(self):
        """Obtenir les statistiques de mémoire"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Nombre total d'interactions
                cursor.execute('SELECT COUNT(*) FROM interactions')
                total_interactions = cursor.fetchone()[0]
                
                # Interactions par speaker
                cursor.execute('''
                    SELECT speaker, COUNT(*) 
                    FROM interactions 
                    GROUP BY speaker
                ''')
                by_speaker = dict(cursor.fetchall())
                
                # Interactions des 7 derniers jours
                week_ago = (datetime.now() - timedelta(days=7)).isoformat()
                cursor.execute('''
                    SELECT COUNT(*) FROM interactions 
                    WHERE timestamp >= ?
                ''', (week_ago,))
                recent_interactions = cursor.fetchone()[0]
                
                # Sessions
                cursor.execute('SELECT COUNT(*) FROM sessions')
                total_sessions = cursor.fetchone()[0]
                
                return {
                    "total_interactions": total_interactions,
                    "by_speaker": by_speaker,
                    "recent_interactions_7days": recent_interactions,
                    "total_sessions": total_sessions,
                    "database_size_mb": self.db_path.stat().st_size / (1024*1024)
                }
                
        except Exception as e:
            self.logger.error(f"Erreur statistiques: {e}")
            return {}
    
    def cleanup_old_data(self, days_to_keep=30):
        """Nettoyer les anciennes données"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Supprimer les anciennes interactions
                cursor.execute('''
                    DELETE FROM interactions WHERE timestamp < ?
                ''', (cutoff_date,))
                
                # Supprimer les anciennes sessions
                cursor.execute('''
                    DELETE FROM sessions WHERE start_time < ?
                ''', (cutoff_date,))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                # Vacuum pour réduire la taille du fichier
                cursor.execute('VACUUM')
                
                self.logger.info(f"Nettoyage: {deleted_count} entrées supprimées")
                return deleted_count
                
        except Exception as e:
            self.logger.error(f"Erreur nettoyage: {e}")
            return 0