# Backend SaaS Ferme Immobilière

## Description

Backend complet pour le SaaS de ferme immobilière développé avec Flask. Cette API REST fournit toutes les fonctionnalités nécessaires pour la gestion immobilière avec intelligence artificielle.

## Fonctionnalités

### 🏠 Gestion des Propriétés
- CRUD complet des propriétés immobilières
- Filtrage par ville, type, prix
- Statistiques automatiques
- Géolocalisation

### 👥 Gestion des Prospects (Leads)
- Système de scoring IA automatique
- Gestion du cycle de vie des prospects
- Filtrage par statut, type, score
- Statistiques de conversion

### 🗺️ Analyse des Quartiers
- Scores de potentiel de farming
- Analyse prédictive IA
- Cartographie interactive
- Recommandations personnalisées

### 📊 Génération de Rapports
- Rapports de marché hyper-localisés
- Prédictions de quartiers
- Profils d'acquéreurs cibles
- Assistant de rédaction IA

### 🤖 Chatbot de Pré-qualification
- Analyse d'intentions automatique
- Génération de leads depuis conversations
- Réponses contextuelles
- Historique des conversations

## Architecture Technique

- **Framework**: Flask 3.1.1
- **Base de données**: SQLite (SQLAlchemy ORM)
- **CORS**: Flask-CORS pour les requêtes cross-origin
- **Structure**: Architecture modulaire avec blueprints
- **IA**: Simulation d'algorithmes de machine learning

## Structure du Projet

```
src/
├── models/          # Modèles de données SQLAlchemy
│   ├── user.py
│   ├── property.py
│   ├── lead.py
│   ├── neighborhood.py
│   └── report.py
├── routes/          # Routes API (blueprints Flask)
│   ├── user.py
│   ├── property.py
│   ├── lead.py
│   ├── neighborhood.py
│   ├── report.py
│   └── chatbot.py
├── static/          # Fichiers statiques (frontend)
├── database/        # Base de données SQLite
│   └── app.db
└── main.py          # Point d'entrée principal
```

## Installation

### Prérequis
- Python 3.11+
- pip

### Étapes d'installation

1. **Cloner ou extraire le projet**
```bash
cd backend-ferme-immo
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
python src/main.py
```

L'API sera accessible sur `http://localhost:5000`

## API Endpoints

### Utilisateurs
- `GET /api/users` - Liste des utilisateurs
- `POST /api/users` - Créer un utilisateur
- `GET /api/users/{id}` - Détails d'un utilisateur
- `PUT /api/users/{id}` - Modifier un utilisateur
- `DELETE /api/users/{id}` - Supprimer un utilisateur

### Propriétés
- `GET /api/properties` - Liste des propriétés (avec filtres)
- `POST /api/properties` - Ajouter une propriété
- `GET /api/properties/{id}` - Détails d'une propriété
- `PUT /api/properties/{id}` - Modifier une propriété
- `DELETE /api/properties/{id}` - Supprimer une propriété
- `GET /api/properties/stats` - Statistiques des propriétés

### Prospects (Leads)
- `GET /api/leads` - Liste des prospects (avec filtres)
- `POST /api/leads` - Créer un prospect
- `GET /api/leads/{id}` - Détails d'un prospect
- `PUT /api/leads/{id}` - Modifier un prospect
- `DELETE /api/leads/{id}` - Supprimer un prospect
- `POST /api/leads/{id}/score` - Recalculer le score
- `GET /api/leads/stats` - Statistiques des prospects

### Quartiers
- `GET /api/quartiers` - Liste des quartiers (avec filtres)
- `POST /api/quartiers` - Ajouter un quartier
- `GET /api/quartiers/{id}` - Détails d'un quartier
- `PUT /api/quartiers/{id}` - Modifier un quartier
- `DELETE /api/quartiers/{id}` - Supprimer un quartier
- `POST /api/quartiers/analyse-predictive` - Analyse IA d'un quartier
- `GET /api/quartiers/cartographie` - Données pour la carte

### Rapports
- `GET /api/rapports` - Liste des rapports
- `POST /api/rapports` - Créer un rapport
- `GET /api/rapports/{id}` - Détails d'un rapport
- `DELETE /api/rapports/{id}` - Supprimer un rapport
- `POST /api/rapports/generer-marche` - Générer rapport de marché
- `POST /api/rapports/assistant-redaction` - Assistant de rédaction

### Chatbot
- `POST /api/chatbot/conversation` - Gérer une conversation
- `GET /api/chatbot/intentions` - Liste des intentions disponibles
- `GET /api/chatbot/conversations` - Historique des conversations

## Exemples d'Utilisation

### Créer une propriété
```bash
curl -X POST http://localhost:5000/api/properties \
  -H "Content-Type: application/json" \
  -d '{
    "address": "15 Rue de la République",
    "city": "Toulouse",
    "postal_code": "31000",
    "property_type": "appartement",
    "surface": 85,
    "rooms": 3,
    "price": 285000,
    "latitude": 43.6047,
    "longitude": 1.4442
  }'
```

### Créer un prospect
```bash
curl -X POST http://localhost:5000/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Marie",
    "last_name": "Dupont",
    "email": "marie.dupont@email.com",
    "phone": "06 12 34 56 78",
    "lead_type": "buyer",
    "budget_min": 250000,
    "budget_max": 350000,
    "property_type_interest": "Appartement 3 pièces",
    "location_interest": "Toulouse Sud"
  }'
```

### Conversation avec le chatbot
```bash
curl -X POST http://localhost:5000/api/chatbot/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bonjour, je cherche à acheter un appartement",
    "session_id": "session_123",
    "contexte": {}
  }'
```

## Fonctionnalités IA Simulées

### Scoring des Prospects
Algorithme de scoring basé sur :
- Budget (poids: élevé)
- Source du lead (poids: moyen)
- Type de prospect (poids: faible)
- Présence de coordonnées (poids: moyen)

### Analyse des Quartiers
Calculs prédictifs basés sur :
- Délai de vente moyen
- Prix au m²
- Données démographiques
- Population

### Génération de Contenu
Assistant IA pour :
- Posts LinkedIn/Facebook
- Descriptions d'annonces
- Slogans marketing
- Optimisation SEO

## Configuration

### Variables d'environnement
```python
# Dans src/main.py
app.config['SECRET_KEY'] = 'ferme-immo-saas-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

### CORS
Le backend est configuré pour accepter les requêtes cross-origin de toutes les origines.

## Déploiement

### Déploiement local
```bash
python src/main.py
```

### Déploiement production
Pour un déploiement en production, considérez :
- Utiliser PostgreSQL au lieu de SQLite
- Configurer un serveur WSGI (Gunicorn)
- Ajouter des variables d'environnement sécurisées
- Implémenter une authentification robuste
- Ajouter des logs et monitoring

## Développement

### Ajouter de nouvelles fonctionnalités
1. Créer le modèle dans `src/models/`
2. Créer les routes dans `src/routes/`
3. Enregistrer le blueprint dans `src/main.py`
4. Tester les endpoints

### Tests
```bash
# Tester l'API
curl http://localhost:5000/api/users
curl http://localhost:5000/api/properties
curl http://localhost:5000/api/leads
```

## Support

Pour toute question ou problème :
- Vérifiez que toutes les dépendances sont installées
- Assurez-vous que le port 5000 est libre
- Consultez les logs dans la console

## Licence

Ce projet est développé pour Pierre Bournet - Spécialiste Immobilier Toulouse Sud.

---

**Version**: 1.0.0  
**Dernière mise à jour**: Mars 2024

