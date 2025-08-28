# Documentation API - SaaS Ferme Immobilière

## Vue d'ensemble

Cette API REST fournit toutes les fonctionnalités nécessaires pour le SaaS de ferme immobilière avec intelligence artificielle.

**Base URL**: `http://localhost:5000/api`

## Authentification

Actuellement, l'API ne nécessite pas d'authentification pour la démonstration. En production, il faudrait implémenter JWT ou OAuth2.

## Format des Réponses

Toutes les réponses sont au format JSON. Les erreurs suivent le format standard HTTP avec des messages explicites.

```json
{
  "error": "Message d'erreur",
  "status": 400
}
```

## Endpoints

### 1. Utilisateurs

#### GET /api/users
Récupère la liste de tous les utilisateurs.

**Réponse**:
```json
[
  {
    "id": 1,
    "username": "pierre.bournet",
    "email": "pierre@example.com"
  }
]
```

#### POST /api/users
Crée un nouvel utilisateur.

**Body**:
```json
{
  "username": "nouveau.user",
  "email": "user@example.com"
}
```

#### GET /api/users/{id}
Récupère un utilisateur par son ID.

#### PUT /api/users/{id}
Met à jour un utilisateur.

#### DELETE /api/users/{id}
Supprime un utilisateur.

---

### 2. Propriétés

#### GET /api/properties
Récupère la liste des propriétés avec filtres optionnels.

**Paramètres de requête**:
- `city` (string): Filtrer par ville
- `property_type` (string): Type de propriété
- `min_price` (number): Prix minimum
- `max_price` (number): Prix maximum

**Exemple**:
```
GET /api/properties?city=Toulouse&property_type=appartement&min_price=200000
```

**Réponse**:
```json
[
  {
    "id": 1,
    "address": "15 Rue de la République",
    "city": "Toulouse",
    "postal_code": "31000",
    "property_type": "appartement",
    "surface": 85,
    "rooms": 3,
    "price": 285000,
    "sale_date": "2024-03-15",
    "latitude": 43.6047,
    "longitude": 1.4442,
    "created_at": "2024-03-01T10:00:00Z",
    "updated_at": "2024-03-01T10:00:00Z"
  }
]
```

#### POST /api/properties
Crée une nouvelle propriété.

**Body**:
```json
{
  "address": "15 Rue de la République",
  "city": "Toulouse",
  "postal_code": "31000",
  "property_type": "appartement",
  "surface": 85,
  "rooms": 3,
  "price": 285000,
  "sale_date": "2024-03-15",
  "latitude": 43.6047,
  "longitude": 1.4442
}
```

#### GET /api/properties/{id}
Récupère une propriété par son ID.

#### PUT /api/properties/{id}
Met à jour une propriété.

#### DELETE /api/properties/{id}
Supprime une propriété.

#### GET /api/properties/stats
Récupère les statistiques des propriétés.

**Paramètres de requête**:
- `city` (string): Filtrer par ville

**Réponse**:
```json
{
  "total_properties": 156,
  "average_price": 325000,
  "average_price_m2": 3200,
  "property_types": {
    "appartement": 89,
    "maison": 45,
    "villa": 22
  }
}
```

---

### 3. Prospects (Leads)

#### GET /api/leads
Récupère la liste des prospects avec filtres.

**Paramètres de requête**:
- `status` (string): Statut du lead
- `lead_type` (string): Type de lead (buyer/seller)
- `min_score` (number): Score minimum

**Réponse**:
```json
[
  {
    "id": 1,
    "first_name": "Marie",
    "last_name": "Dupont",
    "email": "marie.dupont@email.com",
    "phone": "06 12 34 56 78",
    "lead_type": "buyer",
    "budget_min": 250000,
    "budget_max": 350000,
    "property_type_interest": "Appartement 3 pièces",
    "location_interest": "Toulouse Sud",
    "score": 8.5,
    "status": "qualified",
    "source": "website",
    "notes": "Prospect très motivé",
    "created_at": "2024-03-15T10:30:00Z",
    "updated_at": "2024-03-20T14:15:00Z",
    "last_contact_date": "2024-03-20T14:15:00Z"
  }
]
```

#### POST /api/leads
Crée un nouveau prospect.

**Body**:
```json
{
  "first_name": "Marie",
  "last_name": "Dupont",
  "email": "marie.dupont@email.com",
  "phone": "06 12 34 56 78",
  "lead_type": "buyer",
  "budget_min": 250000,
  "budget_max": 350000,
  "property_type_interest": "Appartement 3 pièces",
  "location_interest": "Toulouse Sud",
  "source": "website",
  "notes": "Prospect très motivé"
}
```

#### POST /api/leads/{id}/score
Recalcule le score IA d'un prospect.

**Réponse**:
```json
{
  "score": 8.5
}
```

#### GET /api/leads/stats
Statistiques des prospects.

**Réponse**:
```json
{
  "total_leads": 89,
  "by_status": {
    "new": 15,
    "contacted": 25,
    "qualified": 30,
    "converted": 12,
    "lost": 7
  },
  "by_type": {
    "buyer": 65,
    "seller": 24
  },
  "average_score": 6.8,
  "high_score_leads": 23
}
```

---

### 4. Quartiers

#### GET /api/quartiers
Liste des quartiers avec scores IA.

**Paramètres de requête**:
- `ville` (string): Filtrer par ville
- `score_min` (number): Score minimum

**Réponse**:
```json
[
  {
    "id": 1,
    "name": "Toulouse Sud",
    "city": "Toulouse",
    "postal_code": "31400",
    "latitude": 43.5804,
    "longitude": 1.4481,
    "rotation_rate_score": 8.5,
    "potential_score": 9.2,
    "demand_indicator": 8.8,
    "average_age": 35,
    "average_income": 45000,
    "population": 25000,
    "average_price_m2": 3200,
    "average_sale_time": 45,
    "created_at": "2024-03-01T10:00:00Z",
    "updated_at": "2024-03-01T10:00:00Z"
  }
]
```

#### POST /api/quartiers/analyse-predictive
Analyse IA approfondie d'un quartier.

**Body**:
```json
{
  "quartier_id": 1
}
```

**Réponse**:
```json
{
  "quartier": {
    "id": 1,
    "name": "Toulouse Sud",
    "potential_score": 9.2
  },
  "predictions": {
    "taux_rotation_prevu": 10.2,
    "evolution_prix_6_mois": 8.5,
    "profil_acquereurs_cibles": {
      "type": "Jeunes couples",
      "age_moyen": "28-35 ans",
      "revenus": "45 000 - 65 000 €",
      "preferences": ["2-3 pièces", "Balcon/terrasse", "Parking"],
      "budget_moyen": "280 000 €"
    },
    "recommandations_farming": [
      "Organiser des portes ouvertes le weekend",
      "Distribuer des flyers sur les tendances du marché local",
      "Créer du contenu sur les écoles et services du quartier"
    ]
  },
  "confiance": 0.89
}
```

#### GET /api/quartiers/cartographie
Données pour la cartographie interactive.

**Réponse**:
```json
[
  {
    "id": 1,
    "nom": "Toulouse Sud",
    "ville": "Toulouse",
    "latitude": 43.5804,
    "longitude": 1.4481,
    "score_potentiel": 9.2,
    "score_rotation": 8.5,
    "indicateur_demande": 8.8,
    "prix_m2_moyen": 3200,
    "couleur": "#22c55e"
  }
]
```

---

### 5. Rapports

#### GET /api/rapports
Liste des rapports générés.

**Paramètres de requête**:
- `user_id` (number): Filtrer par utilisateur
- `type` (string): Type de rapport

**Réponse**:
```json
[
  {
    "id": 1,
    "title": "Rapport de Marché - Toulouse Sud",
    "report_type": "analyse_marche",
    "location": "Toulouse Sud",
    "content": "...",
    "file_path": "/reports/marche_toulouse_sud.pdf",
    "status": "completed",
    "user_id": 1,
    "created_at": "2024-03-20T10:30:00Z",
    "updated_at": "2024-03-20T10:35:00Z"
  }
]
```

#### POST /api/rapports/generer-marche
Génère un rapport de marché avec IA.

**Body**:
```json
{
  "location": "Toulouse Sud",
  "user_id": 1
}
```

**Réponse**:
```json
{
  "message": "Rapport généré avec succès",
  "rapport_id": 5,
  "contenu": {
    "titre": "Analyse du Marché Immobilier - Toulouse Sud",
    "date_generation": "2024-03-22T10:30:00Z",
    "resume_executif": {
      "prix_moyen": 325000,
      "evolution_6_mois": 5.2,
      "nombre_transactions": 245,
      "delai_vente_moyen": 52
    },
    "tendances_marche": [
      "Forte demande pour les biens familiaux avec extérieur",
      "Augmentation des prix dans les quartiers résidentiels"
    ],
    "recommandations": [
      "Cibler les propriétaires de maisons individuelles",
      "Développer une stratégie marketing axée sur les familles"
    ]
  }
}
```

#### POST /api/rapports/assistant-redaction
Assistant IA pour la rédaction de contenu.

**Body**:
```json
{
  "type": "post_linkedin",
  "sujet": "Nouvelle analyse de marché",
  "quartier": "Toulouse Sud",
  "mots_cles": ["immobilier", "investissement", "toulouse"]
}
```

**Réponse**:
```json
{
  "type": "post_linkedin",
  "suggestions": [
    "🏡 Découvrez les opportunités exceptionnelles du quartier Toulouse Sud ! Notre analyse IA révèle un potentiel de croissance remarquable. #ImmobilierToulouse #Investissement",
    "💡 Saviez-vous que Toulouse Sud offre un potentiel de plus-value remarquable ? Nouvelle analyse de marché disponible ! #ConseilImmobilier #Expertise"
  ],
  "conseils_seo": [
    "Utilisez les mots-clés 'immobilier, investissement, toulouse' dans les 100 premiers mots",
    "Ajoutez des hashtags locaux pour améliorer la visibilité"
  ],
  "variantes": [
    "🏠 Explorez les opportunités uniques du quartier Toulouse Sud ! Notre analyse IA révèle un potentiel de croissance remarquable. #ImmobilierToulouse #Investissement"
  ]
}
```

---

### 6. Chatbot

#### POST /api/chatbot/conversation
Gère une conversation avec le chatbot IA.

**Body**:
```json
{
  "message": "Bonjour, je cherche à acheter un appartement",
  "session_id": "session_123",
  "contexte": {
    "nb_messages": 1
  }
}
```

**Réponse**:
```json
{
  "reponse": "Parfait ! Vous souhaitez acheter un bien immobilier. Quel type de bien vous intéresse ? (appartement, maison, terrain...)",
  "intention": "recherche_achat",
  "contexte": {
    "type_projet": "achat",
    "nb_messages": 2
  },
  "lead_cree": null,
  "suggestions": [
    "Une maison avec jardin",
    "Un appartement 3 pièces",
    "Dans le centre de Toulouse"
  ],
  "prochaine_question": "Quel est votre budget approximatif pour cet achat ?"
}
```

#### GET /api/chatbot/intentions
Liste des intentions disponibles pour le chatbot.

**Réponse**:
```json
[
  {
    "nom": "salutation",
    "description": "Saluer le chatbot",
    "exemples": ["bonjour", "salut", "hello"]
  },
  {
    "nom": "recherche_achat",
    "description": "Recherche d'un bien à acheter",
    "exemples": ["je cherche à acheter", "je veux acheter une maison"]
  }
]
```

## Codes d'Erreur

- `200` - Succès
- `201` - Créé avec succès
- `204` - Supprimé avec succès
- `400` - Requête invalide
- `404` - Ressource non trouvée
- `500` - Erreur serveur

## Exemples d'Intégration

### JavaScript (Fetch API)
```javascript
// Récupérer les prospects
const leads = await fetch('http://localhost:5000/api/leads')
  .then(response => response.json());

// Créer un nouveau prospect
const newLead = await fetch('http://localhost:5000/api/leads', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    first_name: 'Marie',
    last_name: 'Dupont',
    email: 'marie@example.com',
    lead_type: 'buyer'
  })
}).then(response => response.json());
```

### Python (Requests)
```python
import requests

# Récupérer les quartiers
response = requests.get('http://localhost:5000/api/quartiers')
quartiers = response.json()

# Générer un rapport
rapport_data = {
    'location': 'Toulouse Sud',
    'user_id': 1
}
response = requests.post(
    'http://localhost:5000/api/rapports/generer-marche',
    json=rapport_data
)
rapport = response.json()
```

## Limitations Actuelles

1. **Base de données**: SQLite pour la démonstration (utiliser PostgreSQL en production)
2. **Authentification**: Pas d'authentification (implémenter JWT en production)
3. **IA**: Algorithmes simulés (intégrer de vrais modèles ML en production)
4. **Fichiers**: Pas de stockage de fichiers réel (utiliser cloud storage en production)
5. **Validation**: Validation basique des données (améliorer en production)

## Évolutions Futures

1. Intégration avec des APIs immobilières réelles
2. Modèles de machine learning entraînés
3. Système d'authentification robuste
4. Stockage cloud pour les fichiers
5. Cache Redis pour les performances
6. Tests unitaires et d'intégration
7. Documentation OpenAPI/Swagger

