# J.A.R.V.I.S. - Assistant Vocal Intelligent Local

![J.A.R.V.I.S.](https://img.shields.io/badge/J.A.R.V.I.S.-Opérationnel-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![CUDA](https://img.shields.io/badge/CUDA-Compatible-green)

Assistant vocal intelligent inspiré d'Iron Man, fonctionnant entièrement en local avec support CUDA et RTX 5090.

## 🚀 Caractéristiques

### 🧠 Intelligence Artificielle
- **Ollama local** : Utilise `mistral-small3.2:24b` pour les réponses
- **OpenAI optionnel** : Accès à ChatGPT sur demande
- **Mémoire persistante** : Stockage local des conversations

### 🎤 Synthèse Vocale Avancée
- **Voix William** : Générée avec Tortoise TTS
- **Voix Windows** : Voix système par défaut
- **Commutation vocale** : Changement de voix à la demande

### 📺 Surveillance d'Écran
- **OCR Tesseract** : Lecture du contenu d'écran
- **Analyse contextuelle** : Adaptation des réponses selon l'affichage
- **Détection automatique** : Reconnaissance de logiciels et jeux

### 🏎️ Mécanicien Virtuel SimHub
Conseils de réglage en temps réel pour :
- Assetto Corsa / Assetto Corsa EVO
- Forza Motorsport 8
- Automobilista 2
- Le Mans Ultimate
- F1 2025 (et versions EA précédentes)
- Project CARS 2
- RENNSPORT
- RaceRoom Racing Experience
- KartKraft

### ✈️ Assistant Cockpit DCS F/A-18C
- **Procédures complètes** : Startup, décollage, atterrissage
- **Systèmes d'armes** : Radar, RWR, missiles air-air/air-sol
- **Urgences** : Procédures d'urgence intégrées
- **Guidage vocal** : Instructions étape par étape

## 📋 Prérequis

### Système
- **OS** : Windows 11
- **GPU** : NVIDIA RTX 5090 (CUDA compatible)
- **RAM** : 16 GB minimum (32 GB recommandé)
- **Python** : 3.8+ avec pip

### Logiciels Requis
- **Ollama** : [Installation](https://ollama.ai/)
- **Tesseract OCR** : [Installation Windows](https://github.com/UB-Mannheim/tesseract/wiki)

### Logiciels Optionnels
- **SimHub** : Pour la télémétrie de course
- **DCS World** : Pour l'assistance F/A-18C
- **CrewChief** : Support télémétrie étendu

## 🛠️ Installation

### Installation Automatique
```bash
# 1. Cloner ou décompresser le projet
# 2. Exécuter l'installation
INSTALL_JARVIS.bat
```

### Installation Manuelle
```bash
# Créer l'environnement virtuel
python -m venv jarvis_env
jarvis_env\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Installer PyTorch avec CUDA
pip install torch==2.1.0+cu121 torchaudio==2.1.0+cu121 -f https://download.pytorch.org/whl/cu121/torch_stable.html
```

### Configuration Ollama
```bash
# Démarrer Ollama
ollama serve

# Installer le modèle Mistral
ollama pull mistral-small3.2:24b
```

## 🎯 Utilisation

### Démarrage
```bash
START_JARVIS.bat
```

### Commandes Vocales Principales

#### Contrôle Système
- `"J.A.R.V.I.S., t'es là?"` - Réactivation
- `"Silence"` / `"C'est beau"` - Mode silencieux
- `"Change de voix"` - Basculer William/Windows

#### Intelligence
- `"Utilise ChatGPT"` - Requête OpenAI
- Questions générales - Réponse Mistral local

#### Modules Spécialisés
- `"Analyse l'écran"` - OCR et analyse
- `"Analyse mon tour"` - Conseils SimHub
- `"Active le module F-18"` - Assistant DCS

### Commandes Clavier
Tapez directement vos commandes et appuyez sur Entrée.

## ⚙️ Configuration

### Fichier de Configuration
Éditez `config/config.json` :

```json
{
  "ollama": {
    "model": "mistral-small3.2:24b",
    "url": "http://localhost:11434"
  },
  "openai": {
    "api_key": "VOTRE_CLE_API",
    "model": "gpt-4"
  },
  "voice": {
    "william_voice_path": "voices/william/",
    "tts_engine": "tortoise"
  }
}
```

### Ajout Clé OpenAI (Optionnel)
1. Obtenez une clé API sur [OpenAI](https://platform.openai.com/)
2. Ajoutez-la dans `config/config.json`
3. Redémarrez J.A.R.V.I.S.

## 📁 Structure du Projet

```
JARVIS/
├── jarvis_main.py              # Programme principal
├── modules/                    # Modules fonctionnels
│   ├── voice_manager.py        # Gestion vocale
│   ├── speech_recognition_module.py  # Reconnaissance vocale
│   ├── ollama_client.py        # Client Mistral local
│   ├── openai_client.py        # Client OpenAI
│   ├── screen_monitor.py       # Surveillance écran
│   ├── simhub_mechanic.py      # Mécanicien virtuel
│   ├── dcs_cockpit.py          # Assistant F/A-18
│   └── memory_manager.py       # Gestion mémoire
├── config/
│   └── config.json             # Configuration
├── voices/william/             # Voix Tortoise TTS
├── logs/                       # Journaux
├── memory/                     # Base de données locale
├── screenshots/                # Captures d'écran
├── INSTALL_JARVIS.bat          # Installation automatique
├── START_JARVIS.bat            # Démarrage
└── requirements.txt            # Dépendances Python
```

## 🔧 Dépannage

### Problèmes Courants

#### Ollama non connecté
```bash
# Vérifier le service
curl http://localhost:11434/api/tags

# Redémarrer Ollama
ollama serve
```

#### Erreur Tortoise TTS
- Vérifiez l'installation CUDA
- Testez avec la voix Windows par défaut

#### OCR non fonctionnel
- Installez Tesseract OCR
- Vérifiez le PATH système

#### Microphone non détecté
- Vérifiez les permissions microphone Windows
- Testez avec un autre logiciel de reconnaissance vocale

### Logs et Diagnostics
- **Logs généraux** : `logs/jarvis_YYYYMMDD.log`
- **Logs télémétrie** : `logs/telemetry/`
- **Mémoire conversations** : `memory/jarvis_memory.db`

## 🎮 Intégration Jeux

### SimHub Configuration
1. Installez SimHub
2. Configurez l'export télémétrie (port 8888)
3. Lancez votre jeu de course
4. J.A.R.V.I.S. détectera automatiquement les données

### DCS World F/A-18C
1. Lancez DCS World
2. Sélectionnez le F/A-18C Hornet
3. Dites : `"Active le module F-18"`
4. Demandez de l'aide sur les procédures

## 🔮 Fonctionnalités Avancées

### Personnalisation Voix William
- Ajoutez vos échantillons dans `voices/william/`
- Modifiez `voice_config.json`
- Redémarrez pour appliquer

### Extension Modules
- Créez de nouveaux modules dans `modules/`
- Intégrez-les dans `jarvis_main.py`
- Suivez les patterns existants

## 📊 Performance

### Recommandations Hardware
- **RTX 5090** : Performance optimale Tortoise TTS
- **32 GB RAM** : Chargement rapide des modèles
- **SSD NVMe** : Accès rapide base de données

### Optimisations
- Utilisez la voix Windows pour économiser GPU
- Limitez l'historique mémoire pour les performances
- Ajustez l'intervalle OCR selon vos besoins

## 🤝 Support

### Contact
- **Issues** : Créez un ticket avec logs détaillés
- **Améliorations** : Propositions d'ajout de fonctionnalités
- **Bugs** : Rapport avec reproduction steps

### Contribution
1. Fork du projet
2. Créez une branche feature
3. Testez vos modifications
4. Soumettez une pull request

---

**J.A.R.V.I.S.** - "Just A Rather Very Intelligent System"
*Assistant personnel pour l'ère moderne* 🚀