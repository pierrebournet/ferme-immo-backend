from flask import Blueprint, jsonify, request
from src.models.neighborhood import Neighborhood, db
import random

neighborhood_bp = Blueprint('neighborhood', __name__)

@neighborhood_bp.route('/quartiers', methods=['GET'])
def get_neighborhoods():
    """Récupérer tous les quartiers avec filtres optionnels"""
    ville = request.args.get('ville')
    score_min = request.args.get('score_min', type=float)
    
    query = Neighborhood.query
    
    if ville:
        query = query.filter(Neighborhood.city.ilike(f'%{ville}%'))
    if score_min:
        query = query.filter(Neighborhood.potential_score >= score_min)
    
    # Tri par score de potentiel décroissant
    quartiers = query.order_by(Neighborhood.potential_score.desc()).all()
    return jsonify([quartier.to_dict() for quartier in quartiers])

@neighborhood_bp.route('/quartiers', methods=['POST'])
def create_neighborhood():
    """Créer un nouveau quartier"""
    data = request.json
    
    quartier = Neighborhood(
        name=data['name'],
        city=data['city'],
        postal_code=data.get('postal_code'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        average_age=data.get('average_age'),
        average_income=data.get('average_income'),
        population=data.get('population'),
        average_price_m2=data.get('average_price_m2'),
        average_sale_time=data.get('average_sale_time')
    )
    
    # Calcul des scores (simulation d'IA)
    quartier.rotation_rate_score = calculate_rotation_rate_score(quartier)
    quartier.potential_score = calculate_potential_score(quartier)
    quartier.demand_indicator = calculate_demand_indicator(quartier)
    
    db.session.add(quartier)
    db.session.commit()
    return jsonify(quartier.to_dict()), 201

@neighborhood_bp.route('/quartiers/<int:quartier_id>', methods=['GET'])
def get_neighborhood(quartier_id):
    """Récupérer un quartier par son ID"""
    quartier = Neighborhood.query.get_or_404(quartier_id)
    return jsonify(quartier.to_dict())

@neighborhood_bp.route('/quartiers/<int:quartier_id>', methods=['PUT'])
def update_neighborhood(quartier_id):
    """Mettre à jour un quartier"""
    quartier = Neighborhood.query.get_or_404(quartier_id)
    data = request.json
    
    quartier.name = data.get('name', quartier.name)
    quartier.city = data.get('city', quartier.city)
    quartier.postal_code = data.get('postal_code', quartier.postal_code)
    quartier.latitude = data.get('latitude', quartier.latitude)
    quartier.longitude = data.get('longitude', quartier.longitude)
    quartier.average_age = data.get('average_age', quartier.average_age)
    quartier.average_income = data.get('average_income', quartier.average_income)
    quartier.population = data.get('population', quartier.population)
    quartier.average_price_m2 = data.get('average_price_m2', quartier.average_price_m2)
    quartier.average_sale_time = data.get('average_sale_time', quartier.average_sale_time)
    
    # Recalcul des scores
    quartier.rotation_rate_score = calculate_rotation_rate_score(quartier)
    quartier.potential_score = calculate_potential_score(quartier)
    quartier.demand_indicator = calculate_demand_indicator(quartier)
    
    db.session.commit()
    return jsonify(quartier.to_dict())

@neighborhood_bp.route('/quartiers/<int:quartier_id>', methods=['DELETE'])
def delete_neighborhood(quartier_id):
    """Supprimer un quartier"""
    quartier = Neighborhood.query.get_or_404(quartier_id)
    db.session.delete(quartier)
    db.session.commit()
    return '', 204

@neighborhood_bp.route('/quartiers/analyse-predictive', methods=['POST'])
def analyze_neighborhood():
    """Analyser un quartier avec l'IA prédictive"""
    data = request.json
    quartier_id = data.get('quartier_id')
    
    if not quartier_id:
        return jsonify({'erreur': 'ID du quartier requis'}), 400
    
    quartier = Neighborhood.query.get_or_404(quartier_id)
    
    # Simulation d'analyse IA avancée
    analyse = {
        'quartier': quartier.to_dict(),
        'predictions': {
            'taux_rotation_prevu': round(quartier.rotation_rate_score * 1.2, 2),
            'evolution_prix_6_mois': random.uniform(-5, 15),
            'profil_acquereurs_cibles': generate_buyer_profile(quartier),
            'recommandations_farming': generate_farming_recommendations(quartier)
        },
        'confiance': random.uniform(0.75, 0.95)
    }
    
    return jsonify(analyse)

@neighborhood_bp.route('/quartiers/cartographie', methods=['GET'])
def get_neighborhood_map_data():
    """Obtenir les données pour la cartographie interactive"""
    quartiers = Neighborhood.query.all()
    
    map_data = []
    for quartier in quartiers:
        if quartier.latitude and quartier.longitude:
            map_data.append({
                'id': quartier.id,
                'nom': quartier.name,
                'ville': quartier.city,
                'latitude': quartier.latitude,
                'longitude': quartier.longitude,
                'score_potentiel': quartier.potential_score,
                'score_rotation': quartier.rotation_rate_score,
                'indicateur_demande': quartier.demand_indicator,
                'prix_m2_moyen': quartier.average_price_m2,
                'couleur': get_score_color(quartier.potential_score)
            })
    
    return jsonify(map_data)

def calculate_rotation_rate_score(quartier):
    """Calculer le score de taux de rotation (simulation d'IA)"""
    score = 5.0
    
    if quartier.average_sale_time and quartier.average_sale_time < 60:
        score += 2.0
    if quartier.average_price_m2 and quartier.average_price_m2 < 3000:
        score += 1.5
    if quartier.population and quartier.population > 10000:
        score += 1.0
    
    score += random.uniform(-1, 2)
    return max(0, min(10, round(score, 1)))

def calculate_potential_score(quartier):
    """Calculer le score de potentiel de farming (simulation d'IA)"""
    score = 5.0
    
    if quartier.rotation_rate_score:
        score += quartier.rotation_rate_score * 0.3
    if quartier.average_income and quartier.average_income > 35000:
        score += 1.5
    if quartier.average_age and 30 <= quartier.average_age <= 45:
        score += 1.0
    
    score += random.uniform(-0.5, 1.5)
    return max(0, min(10, round(score, 1)))

def calculate_demand_indicator(quartier):
    """Calculer l'indicateur de demande (simulation d'IA)"""
    score = 5.0
    
    if quartier.average_price_m2:
        if quartier.average_price_m2 < 2500:
            score += 2.0
        elif quartier.average_price_m2 < 4000:
            score += 1.0
    
    score += random.uniform(-1, 2)
    return max(0, min(10, round(score, 1)))

def generate_buyer_profile(quartier):
    """Générer un profil d'acquéreurs cibles (simulation d'IA)"""
    profiles = [
        {
            'type': 'Jeunes couples',
            'age_moyen': '28-35 ans',
            'revenus': '45 000 - 65 000 €',
            'preferences': 'Appartements 2-3 pièces, proximité transports',
            'budget_moyen': '250 000 - 350 000 €'
        },
        {
            'type': 'Familles avec enfants',
            'age_moyen': '35-45 ans',
            'revenus': '55 000 - 80 000 €',
            'preferences': 'Maisons avec jardin, quartiers résidentiels',
            'budget_moyen': '350 000 - 500 000 €'
        },
        {
            'type': 'Investisseurs locatifs',
            'age_moyen': '40-55 ans',
            'revenus': '60 000 - 100 000 €',
            'preferences': 'Rendement locatif, proximité universités/centres',
            'budget_moyen': '200 000 - 400 000 €'
        }
    ]
    
    return random.choice(profiles)

def generate_farming_recommendations(quartier):
    """Générer des recommandations de farming (simulation d'IA)"""
    recommendations = [
        'Organiser des portes ouvertes le weekend',
        'Distribuer des flyers sur les tendances du marché local',
        'Créer du contenu sur les écoles et services du quartier',
        'Développer un réseau avec les commerces locaux',
        'Organiser des événements de quartier',
        'Proposer des évaluations gratuites aux propriétaires'
    ]
    
    return random.sample(recommendations, 3)

def get_score_color(score):
    """Obtenir la couleur basée sur le score"""
    if score >= 8:
        return '#22c55e'  # Vert
    elif score >= 6:
        return '#f59e0b'  # Orange
    elif score >= 4:
        return '#ef4444'  # Rouge
    else:
        return '#6b7280'  # Gris

