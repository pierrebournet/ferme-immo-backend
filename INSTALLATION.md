# Guide d'Installation - Backend SaaS Ferme Immobilière

## Prérequis Système

### Logiciels Requis
- **Python 3.11 ou supérieur**
- **pip** (gestionnaire de paquets Python)
- **Git** (optionnel, pour le versioning)

### Vérification des Prérequis
```bash
# Vérifier Python
python --version
# ou
python3 --version

# Vérifier pip
pip --version
# ou
pip3 --version
```

## Installation Étape par Étape

### 1. Préparation de l'Environnement

#### Créer un Dossier de Projet
```bash
mkdir ferme-immo-backend
cd ferme-immo-backend
```

#### Extraire les Fichiers
Copiez tous les fichiers du backend dans ce dossier :
- `src/` (dossier complet)
- `requirements.txt`
- `README.md`
- `API_DOCUMENTATION.md`
- `INSTALLATION.md`

### 2. Environnement Virtuel Python

#### Créer l'Environnement Virtuel
```bash
# Linux/Mac
python3 -m venv venv

# Windows
python -m venv venv
```

#### Activer l'Environnement Virtuel
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Vous devriez voir `(venv)` au début de votre ligne de commande.

### 3. Installation des Dépendances

```bash
pip install -r requirements.txt
```

#### Dépendances Principales
- `Flask==3.1.1` - Framework web
- `Flask-SQLAlchemy==3.1.1` - ORM pour base de données
- `Flask-CORS==6.0.0` - Support CORS
- `Werkzeug==3.1.3` - Utilitaires WSGI

### 4. Configuration de la Base de Données

La base de données SQLite sera créée automatiquement au premier lancement.

#### Structure Créée Automatiquement
```
src/database/
└── app.db  # Base de données SQLite
```

### 5. Premier Lancement

```bash
python src/main.py
```

#### Sortie Attendue
```
 * Serving Flask app 'main'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 6. Vérification de l'Installation

#### Test de Base
```bash
curl http://localhost:5000/api/users
```

Réponse attendue : `[]` (liste vide)

#### Test Complet
```bash
# Tester les différents endpoints
curl http://localhost:5000/api/properties
curl http://localhost:5000/api/leads
curl http://localhost:5000/api/quartiers
curl http://localhost:5000/api/rapports
```

## Configuration Avancée

### Variables d'Environnement

Créer un fichier `.env` (optionnel) :
```bash
# .env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=votre-clé-secrète-ici
DATABASE_URL=sqlite:///database/app.db
```

### Configuration de Production

#### 1. Désactiver le Mode Debug
Dans `src/main.py`, modifier :
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

#### 2. Utiliser un Serveur WSGI
```bash
pip install gunicorn

# Lancer avec Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

#### 3. Base de Données PostgreSQL
```bash
pip install psycopg2-binary

# Modifier la configuration dans main.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
```

## Résolution des Problèmes

### Problème : Port 5000 Occupé
```bash
# Trouver le processus utilisant le port
lsof -i :5000

# Ou utiliser un autre port
python src/main.py --port 5001
```

### Problème : Erreur d'Import
```bash
# Vérifier que l'environnement virtuel est activé
which python

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### Problème : Base de Données
```bash
# Supprimer et recréer la base
rm src/database/app.db
python src/main.py
```

### Problème : CORS
Si vous avez des erreurs CORS avec votre frontend :
```python
# Dans src/main.py, vérifier que CORS est configuré
from flask_cors import CORS
CORS(app)
```

## Structure des Fichiers

```
backend-ferme-immo/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── property.py
│   │   ├── lead.py
│   │   ├── neighborhood.py
│   │   └── report.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── property.py
│   │   ├── lead.py
│   │   ├── neighborhood.py
│   │   ├── report.py
│   │   └── chatbot.py
│   ├── static/
│   │   └── index.html
│   ├── database/
│   │   └── app.db
│   └── main.py
├── venv/
├── requirements.txt
├── README.md
├── API_DOCUMENTATION.md
└── INSTALLATION.md
```

## Tests de Fonctionnement

### Script de Test Automatique
Créer un fichier `test_api.py` :
```python
import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_endpoints():
    endpoints = [
        '/users',
        '/properties',
        '/leads',
        '/quartiers',
        '/rapports'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print(f"✅ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

if __name__ == '__main__':
    test_endpoints()
```

Exécuter :
```bash
python test_api.py
```

### Test de Création de Données
```bash
# Créer un utilisateur
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com"}'

# Créer une propriété
curl -X POST http://localhost:5000/api/properties \
  -H "Content-Type: application/json" \
  -d '{
    "address": "Test Address",
    "city": "Toulouse",
    "postal_code": "31000",
    "property_type": "appartement",
    "surface": 75,
    "rooms": 3,
    "price": 250000
  }'
```

## Maintenance

### Sauvegarde de la Base de Données
```bash
# Copier la base SQLite
cp src/database/app.db backup_$(date +%Y%m%d).db
```

### Mise à Jour des Dépendances
```bash
pip list --outdated
pip install --upgrade package_name
pip freeze > requirements.txt
```

### Logs et Monitoring
```bash
# Lancer avec logs
python src/main.py > app.log 2>&1 &

# Suivre les logs
tail -f app.log
```

## Support et Aide

### Commandes Utiles
```bash
# Vérifier l'état du serveur
ps aux | grep python

# Arrêter le serveur
pkill -f "python src/main.py"

# Redémarrer
python src/main.py &
```

### Ressources
- Documentation Flask : https://flask.palletsprojects.com/
- Documentation SQLAlchemy : https://docs.sqlalchemy.org/
- Guide CORS : https://flask-cors.readthedocs.io/

### Contact
Pour toute question technique, consultez :
1. Ce guide d'installation
2. La documentation API (`API_DOCUMENTATION.md`)
3. Le README principal (`README.md`)

---

**Installation réussie ?** Votre API devrait être accessible sur `http://localhost:5000/api`

