#!/bin/bash

echo "🚀 Démarrage du Backend SaaS Ferme Immobilière"
echo "=============================================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📚 Installation des dépendances..."
pip install -r requirements.txt

# Créer le dossier de base de données s'il n'existe pas
mkdir -p src/database

# Démarrer l'application
echo "🌟 Démarrage de l'application..."
echo "📡 API disponible sur : http://localhost:5000/api"
echo "📖 Documentation : README.md"
echo "🛠️  Pour arrêter : Ctrl+C"
echo ""

python src/main.py
