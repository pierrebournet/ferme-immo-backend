# Architecture du Backend - SaaS Ferme Immobilière

## Vue d'Ensemble

Le backend est conçu selon une architecture modulaire basée sur Flask, avec une séparation claire entre les modèles de données, les routes API et la logique métier.

## Architecture Générale

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Backend       │
│   (React)       │◄──►│   (Flask)       │◄──►│   (SQLAlchemy)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (SQLite)      │
                       └─────────────────┘
```

## Structure des Dossiers

```
src/
├── main.py              # Point d'entrée principal
├── models/              # Modèles de données (SQLAlchemy)
│   ├── user.py         # Modèle utilisateur
│   ├── property.py     # Modèle propriété
│   ├── lead.py         # Modèle prospect
│   ├── neighborhood.py # Modèle quartier
│   └── report.py       # Modèle rapport
├── routes/              # Routes API (Flask Blueprints)
│   ├── user.py         # Routes utilisateurs
│   ├── property.py     # Routes propriétés
│   ├── lead.py         # Routes prospects
│   ├── neighborhood.py # Routes quartiers
│   ├── report.py       # Routes rapports
│   └── chatbot.py      # Routes chatbot
├── static/              # Fichiers statiques
└── database/            # Base de données
    └── app.db          # SQLite database
```

## Couches de l'Application

### 1. Couche de Présentation (API)
- **Responsabilité** : Exposition des endpoints REST
- **Technologies** : Flask, Flask-CORS
- **Fichiers** : `routes/*.py`

#### Blueprints Flask
Chaque module fonctionnel est organisé en blueprint :
```python
# Exemple : routes/property.py
from flask import Blueprint
property_bp = Blueprint('property', __name__)

@property_bp.route('/properties', methods=['GET'])
def get_properties():
    # Logique de récupération
```

### 2. Couche Métier (Business Logic)
- **Responsabilité** : Logique applicative et règles métier
- **Technologies** : Python pur
- **Localisation** : Intégrée dans les routes

#### Fonctionnalités IA Simulées
```python
def calculate_lead_score(lead):
    """Calcul du score de prospect avec IA simulée"""
    score = 5.0  # Score de base
    
    # Facteurs d'influence
    if lead.budget_min and lead.budget_min > 200000:
        score += 1.5
    if lead.phone:
        score += 0.5
    
    return max(0, min(10, round(score, 1)))
```

### 3. Couche de Données (Data Access)
- **Responsabilité** : Accès et persistance des données
- **Technologies** : SQLAlchemy ORM
- **Fichiers** : `models/*.py`

#### Modèles de Données
```python
# Exemple : models/property.py
class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float)
    # ... autres champs
```

### 4. Couche de Persistance
- **Responsabilité** : Stockage des données
- **Technologies** : SQLite (développement), PostgreSQL (production)
- **Fichier** : `database/app.db`

## Modèles de Données

### Schéma de Base de Données

```sql
-- Utilisateurs
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);

-- Propriétés
CREATE TABLE property (
    id INTEGER PRIMARY KEY,
    address VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    property_type VARCHAR(50) NOT NULL,
    surface FLOAT,
    rooms INTEGER,
    price FLOAT,
    sale_date DATE,
    latitude FLOAT,
    longitude FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Prospects
CREATE TABLE lead (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20),
    lead_type VARCHAR(20) NOT NULL,
    budget_min FLOAT,
    budget_max FLOAT,
    property_type_interest VARCHAR(100),
    location_interest VARCHAR(200),
    score FLOAT DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'new',
    source VARCHAR(50),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_contact_date DATETIME
);

-- Quartiers
CREATE TABLE neighborhood (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(10),
    latitude FLOAT,
    longitude FLOAT,
    rotation_rate_score FLOAT DEFAULT 0.0,
    potential_score FLOAT DEFAULT 0.0,
    demand_indicator FLOAT DEFAULT 0.0,
    average_age FLOAT,
    average_income FLOAT,
    population INTEGER,
    average_price_m2 FLOAT,
    average_sale_time INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Rapports
CREATE TABLE report (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    location VARCHAR(200),
    content TEXT,
    file_path VARCHAR(500),
    status VARCHAR(20) DEFAULT 'generating',
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
```

### Relations entre Modèles

```
User (1) ──────────── (N) Report
                      
Property (N) ──────── (1) Neighborhood (implicite par localisation)

Lead (indépendant)

Neighborhood (indépendant)
```

## APIs et Endpoints

### Structure des URLs
```
/api/
├── users/              # Gestion utilisateurs
├── properties/         # Gestion propriétés
│   └── stats          # Statistiques
├── leads/              # Gestion prospects
│   ├── {id}/score     # Recalcul score
│   └── stats          # Statistiques
├── quartiers/          # Gestion quartiers
│   ├── analyse-predictive  # Analyse IA
│   └── cartographie   # Données carte
├── rapports/           # Gestion rapports
│   ├── generer-marche # Génération rapport marché
│   └── assistant-redaction  # Assistant IA
└── chatbot/            # Chatbot IA
    ├── conversation   # Gestion conversation
    ├── intentions     # Liste intentions
    └── conversations  # Historique
```

### Formats de Réponse Standardisés

#### Succès
```json
{
  "data": [...],
  "status": "success",
  "message": "Opération réussie"
}
```

#### Erreur
```json
{
  "error": "Message d'erreur détaillé",
  "status": "error",
  "code": 400
}
```

## Fonctionnalités IA

### 1. Scoring des Prospects
```python
def calculate_lead_score(lead):
    """
    Algorithme de scoring basé sur :
    - Budget (poids: 30%)
    - Source (poids: 25%)
    - Coordonnées complètes (poids: 20%)
    - Type de prospect (poids: 15%)
    - Facteur aléatoire (poids: 10%)
    """
```

### 2. Analyse des Quartiers
```python
def calculate_potential_score(neighborhood):
    """
    Score de potentiel basé sur :
    - Taux de rotation (poids: 40%)
    - Revenus moyens (poids: 30%)
    - Âge de la population (poids: 20%)
    - Facteur aléatoire (poids: 10%)
    """
```

### 3. Génération de Contenu
```python
def generer_suggestions_contenu(type_contenu, sujet, quartier, mots_cles):
    """
    Génération de contenu pour :
    - Posts LinkedIn/Facebook
    - Descriptions d'annonces
    - Slogans marketing
    - Conseils SEO
    """
```

### 4. Chatbot Conversationnel
```python
def analyser_intention(message):
    """
    Analyse d'intention basée sur :
    - Mots-clés prédéfinis
    - Expressions régulières
    - Contexte de conversation
    """
```

## Configuration et Déploiement

### Configuration de Développement
```python
# src/main.py
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/app.db'
app.config['SECRET_KEY'] = 'dev-key'
```

### Configuration de Production
```python
app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
```

### Déploiement avec Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 5000

CMD ["python", "src/main.py"]
```

## Sécurité

### Mesures Implémentées
- **CORS** : Configuration pour requêtes cross-origin
- **Validation** : Validation basique des données d'entrée
- **ORM** : Protection contre l'injection SQL via SQLAlchemy

### Améliorations Recommandées
- **Authentification JWT** : Tokens sécurisés
- **Rate Limiting** : Limitation des requêtes
- **Validation Avancée** : Marshmallow ou Pydantic
- **Logs de Sécurité** : Audit trail complet

## Performance et Scalabilité

### Optimisations Actuelles
- **ORM Efficace** : Requêtes optimisées SQLAlchemy
- **Structure Modulaire** : Blueprints pour la séparation
- **Réponses JSON** : Format léger

### Améliorations Futures
- **Cache Redis** : Cache des requêtes fréquentes
- **Pagination** : Limitation des résultats
- **Index Database** : Index sur colonnes fréquemment utilisées
- **CDN** : Distribution de contenu statique

## Tests et Qualité

### Structure de Tests Recommandée
```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_routes.py
│   └── test_ai_functions.py
├── integration/
│   ├── test_api_endpoints.py
│   └── test_database.py
└── fixtures/
    └── sample_data.py
```

### Métriques de Qualité
- **Couverture de Code** : Objectif 80%+
- **Tests Unitaires** : Chaque fonction métier
- **Tests d'Intégration** : Chaque endpoint API
- **Tests de Performance** : Temps de réponse < 200ms

## Monitoring et Logs

### Logs Recommandés
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Métriques à Surveiller
- **Temps de Réponse** : API endpoints
- **Utilisation Mémoire** : Processus Python
- **Requêtes/Seconde** : Charge serveur
- **Erreurs 5xx** : Erreurs serveur
- **Taille Base de Données** : Croissance des données

## Évolution et Maintenance

### Roadmap Technique
1. **Phase 1** : Authentification JWT
2. **Phase 2** : Cache Redis
3. **Phase 3** : Base PostgreSQL
4. **Phase 4** : Vrais modèles ML
5. **Phase 5** : Microservices

### Bonnes Pratiques
- **Versioning API** : `/api/v1/`, `/api/v2/`
- **Documentation** : Swagger/OpenAPI
- **CI/CD** : Tests automatisés
- **Backup** : Sauvegarde régulière BDD
- **Monitoring** : Alertes proactives

