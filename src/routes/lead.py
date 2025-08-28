from flask import Blueprint, jsonify, request
from src.models.lead import Lead, db
from datetime import datetime
import random

lead_bp = Blueprint('lead', __name__)

@lead_bp.route('/leads', methods=['GET'])
def get_leads():
    """Récupérer tous les leads avec filtres optionnels"""
    status = request.args.get('status')
    lead_type = request.args.get('lead_type')
    min_score = request.args.get('min_score', type=float)
    
    query = Lead.query
    
    if status:
        query = query.filter(Lead.status == status)
    if lead_type:
        query = query.filter(Lead.lead_type == lead_type)
    if min_score:
        query = query.filter(Lead.score >= min_score)
    
    # Tri par score décroissant par défaut
    leads = query.order_by(Lead.score.desc()).all()
    return jsonify([lead.to_dict() for lead in leads])

@lead_bp.route('/leads', methods=['POST'])
def create_lead():
    """Créer un nouveau lead"""
    data = request.json
    
    lead = Lead(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone'),
        lead_type=data['lead_type'],
        budget_min=data.get('budget_min'),
        budget_max=data.get('budget_max'),
        property_type_interest=data.get('property_type_interest'),
        location_interest=data.get('location_interest'),
        source=data.get('source'),
        notes=data.get('notes')
    )
    
    # Calcul du score initial (simulation d'IA)
    lead.score = calculate_lead_score(lead)
    
    db.session.add(lead)
    db.session.commit()
    return jsonify(lead.to_dict()), 201

@lead_bp.route('/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Récupérer un lead par son ID"""
    lead = Lead.query.get_or_404(lead_id)
    return jsonify(lead.to_dict())

@lead_bp.route('/leads/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    """Mettre à jour un lead"""
    lead = Lead.query.get_or_404(lead_id)
    data = request.json
    
    lead.first_name = data.get('first_name', lead.first_name)
    lead.last_name = data.get('last_name', lead.last_name)
    lead.email = data.get('email', lead.email)
    lead.phone = data.get('phone', lead.phone)
    lead.lead_type = data.get('lead_type', lead.lead_type)
    lead.budget_min = data.get('budget_min', lead.budget_min)
    lead.budget_max = data.get('budget_max', lead.budget_max)
    lead.property_type_interest = data.get('property_type_interest', lead.property_type_interest)
    lead.location_interest = data.get('location_interest', lead.location_interest)
    lead.status = data.get('status', lead.status)
    lead.source = data.get('source', lead.source)
    lead.notes = data.get('notes', lead.notes)
    
    # Recalcul du score si nécessaire
    if any(key in data for key in ['budget_min', 'budget_max', 'lead_type', 'source']):
        lead.score = calculate_lead_score(lead)
    
    db.session.commit()
    return jsonify(lead.to_dict())

@lead_bp.route('/leads/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    """Supprimer un lead"""
    lead = Lead.query.get_or_404(lead_id)
    db.session.delete(lead)
    db.session.commit()
    return '', 204

@lead_bp.route('/leads/<int:lead_id>/score', methods=['POST'])
def recalculate_lead_score(lead_id):
    """Recalculer le score d'un lead"""
    lead = Lead.query.get_or_404(lead_id)
    lead.score = calculate_lead_score(lead)
    db.session.commit()
    return jsonify({'score': lead.score})

@lead_bp.route('/leads/stats', methods=['GET'])
def get_lead_stats():
    """Obtenir des statistiques sur les leads"""
    leads = Lead.query.all()
    
    if not leads:
        return jsonify({
            'total_leads': 0,
            'by_status': {},
            'by_type': {},
            'average_score': 0,
            'high_score_leads': 0
        })
    
    total_leads = len(leads)
    
    # Statistiques par statut
    by_status = {}
    for lead in leads:
        by_status[lead.status] = by_status.get(lead.status, 0) + 1
    
    # Statistiques par type
    by_type = {}
    for lead in leads:
        by_type[lead.lead_type] = by_type.get(lead.lead_type, 0) + 1
    
    # Score moyen
    scores = [lead.score for lead in leads if lead.score]
    average_score = sum(scores) / len(scores) if scores else 0
    
    # Leads avec score élevé (> 7)
    high_score_leads = len([lead for lead in leads if lead.score > 7])
    
    return jsonify({
        'total_leads': total_leads,
        'by_status': by_status,
        'by_type': by_type,
        'average_score': round(average_score, 2),
        'high_score_leads': high_score_leads
    })

def calculate_lead_score(lead):
    """Calculer le score d'un lead (simulation d'IA)"""
    score = 5.0  # Score de base
    
    # Facteurs positifs
    if lead.budget_min and lead.budget_min > 200000:
        score += 1.5
    if lead.budget_max and lead.budget_max > 400000:
        score += 1.0
    if lead.phone:
        score += 0.5
    if lead.source in ['website', 'referral']:
        score += 1.0
    if lead.lead_type == 'buyer':
        score += 0.5
    
    # Ajout d'un facteur aléatoire pour simuler l'IA
    score += random.uniform(-0.5, 1.5)
    
    # Limiter le score entre 0 et 10
    return max(0, min(10, round(score, 1)))

