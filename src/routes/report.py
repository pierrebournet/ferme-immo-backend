from flask import Blueprint, jsonify, request
from src.models.report import Report, db
from src.models.neighborhood import Neighborhood
from src.models.property import Property
import json
from datetime import datetime, timedelta
import random

report_bp = Blueprint('report', __name__)

@report_bp.route('/rapports', methods=['GET'])
def get_reports():
    """Récupérer tous les rapports"""
    user_id = request.args.get('user_id', type=int)
    report_type = request.args.get('type')
    
    query = Report.query
    
    if user_id:
        query = query.filter(Report.user_id == user_id)
    if report_type:
        query = query.filter(Report.report_type == report_type)
    
    rapports = query.order_by(Report.created_at.desc()).all()
    return jsonify([rapport.to_dict() for rapport in rapports])

@report_bp.route('/rapports', methods=['POST'])
def create_report():
    """Créer un nouveau rapport"""
    data = request.json
    
    rapport = Report(
        title=data['title'],
        report_type=data['report_type'],
        location=data.get('location'),
        user_id=data['user_id'],
        status='generating'
    )
    
    db.session.add(rapport)
    db.session.commit()
    
    # Générer le contenu du rapport selon le type
    if rapport.report_type == 'analyse_marche':
        contenu = generer_rapport_marche(rapport.location)
    elif rapport.report_type == 'prediction_quartier':
        contenu = generer_rapport_prediction(rapport.location)
    elif rapport.report_type == 'profil_acquereurs':
        contenu = generer_rapport_profils(rapport.location)
    else:
        contenu = {'erreur': 'Type de rapport non supporté'}
    
    rapport.content = json.dumps(contenu, ensure_ascii=False)
    rapport.status = 'completed'
    
    db.session.commit()
    return jsonify(rapport.to_dict()), 201

@report_bp.route('/rapports/<int:rapport_id>', methods=['GET'])
def get_report(rapport_id):
    """Récupérer un rapport par son ID"""
    rapport = Report.query.get_or_404(rapport_id)
    
    # Convertir le contenu JSON en objet Python
    rapport_dict = rapport.to_dict()
    if rapport.content:
        try:
            rapport_dict['content'] = json.loads(rapport.content)
        except json.JSONDecodeError:
            rapport_dict['content'] = {'erreur': 'Contenu invalide'}
    
    return jsonify(rapport_dict)

@report_bp.route('/rapports/<int:rapport_id>', methods=['DELETE'])
def delete_report(rapport_id):
    """Supprimer un rapport"""
    rapport = Report.query.get_or_404(rapport_id)
    db.session.delete(rapport)
    db.session.commit()
    return '', 204

@report_bp.route('/rapports/generer-marche', methods=['POST'])
def generate_market_report():
    """Générer un rapport de marché hyper-localisé"""
    data = request.json
    location = data.get('location', 'Toulouse Sud')
    user_id = data.get('user_id', 1)
    
    # Créer le rapport
    rapport = Report(
        title=f'Rapport de Marché - {location}',
        report_type='analyse_marche',
        location=location,
        user_id=user_id,
        status='generating'
    )
    
    db.session.add(rapport)
    db.session.commit()
    
    # Générer le contenu
    contenu = generer_rapport_marche(location)
    rapport.content = json.dumps(contenu, ensure_ascii=False)
    rapport.status = 'completed'
    
    db.session.commit()
    
    return jsonify({
        'message': 'Rapport généré avec succès',
        'rapport_id': rapport.id,
        'contenu': contenu
    })

@report_bp.route('/rapports/assistant-redaction', methods=['POST'])
def content_writing_assistant():
    """Assistant de rédaction pour les réseaux sociaux et annonces"""
    data = request.json
    type_contenu = data.get('type', 'post_linkedin')  # post_linkedin, post_facebook, annonce, slogan
    sujet = data.get('sujet', '')
    quartier = data.get('quartier', '')
    mots_cles = data.get('mots_cles', [])
    
    suggestions = generer_suggestions_contenu(type_contenu, sujet, quartier, mots_cles)
    
    return jsonify({
        'type': type_contenu,
        'suggestions': suggestions,
        'conseils_seo': generer_conseils_seo(mots_cles),
        'variantes': generer_variantes_messages(suggestions[0] if suggestions else '')
    })

def generer_rapport_marche(location):
    """Générer le contenu d'un rapport de marché (simulation d'IA)"""
    # Récupérer des données réelles de la base
    proprietes = Property.query.filter(Property.city.ilike(f'%{location}%')).all()
    quartiers = Neighborhood.query.filter(Neighborhood.city.ilike(f'%{location}%')).all()
    
    # Calculer des statistiques
    if proprietes:
        prix_moyen = sum([p.price for p in proprietes if p.price]) / len([p for p in proprietes if p.price])
        surface_moyenne = sum([p.surface for p in proprietes if p.surface]) / len([p for p in proprietes if p.surface])
    else:
        prix_moyen = random.uniform(250000, 450000)
        surface_moyenne = random.uniform(70, 120)
    
    return {
        'titre': f'Analyse du Marché Immobilier - {location}',
        'date_generation': datetime.now().isoformat(),
        'resume_executif': {
            'prix_moyen': round(prix_moyen, 0),
            'evolution_6_mois': round(random.uniform(-3, 8), 1),
            'nombre_transactions': len(proprietes) if proprietes else random.randint(150, 300),
            'delai_vente_moyen': random.randint(45, 90)
        },
        'tendances_marche': [
            'Forte demande pour les biens familiaux avec extérieur',
            'Augmentation des prix dans les quartiers résidentiels',
            'Développement des infrastructures de transport',
            'Intérêt croissant des investisseurs locatifs'
        ],
        'analyse_quartiers': [q.to_dict() for q in quartiers[:5]] if quartiers else [],
        'recommandations': [
            'Cibler les propriétaires de maisons individuelles',
            'Développer une stratégie marketing axée sur les familles',
            'Mettre en avant la qualité de vie du secteur',
            'Organiser des événements de networking local'
        ],
        'previsions': {
            'evolution_prix_12_mois': round(random.uniform(2, 12), 1),
            'secteurs_porteurs': ['Centre-ville rénové', 'Quartiers résidentiels', 'Proximité métro'],
            'opportunites_investissement': 'Forte demande locative étudiante et jeunes actifs'
        }
    }

def generer_rapport_prediction(location):
    """Générer un rapport de prédiction de quartier (simulation d'IA)"""
    return {
        'titre': f'Prédictions Immobilières - {location}',
        'date_generation': datetime.now().isoformat(),
        'modele_ia': 'Vertex AI - Prédiction Immobilière v2.1',
        'confiance': round(random.uniform(0.82, 0.94), 2),
        'predictions': {
            'taux_rotation_6_mois': round(random.uniform(8, 15), 1),
            'evolution_demande': 'Hausse modérée (+12%)',
            'profil_acquereurs_dominants': 'Familles 35-45 ans, revenus 55-75k€',
            'meilleure_periode_farming': 'Mars-Mai et Septembre-Novembre'
        },
        'facteurs_influence': [
            {'facteur': 'Proximité écoles', 'impact': 8.5},
            {'facteur': 'Transports en commun', 'impact': 7.2},
            {'facteur': 'Commerces de proximité', 'impact': 6.8},
            {'facteur': 'Espaces verts', 'impact': 6.1}
        ],
        'alertes': [
            'Nouveau projet de tramway prévu pour 2025',
            'Ouverture d\'un centre commercial en 2024',
            'Rénovation urbaine du centre-ville en cours'
        ]
    }

def generer_rapport_profils(location):
    """Générer un rapport de profils d'acquéreurs (simulation d'IA)"""
    return {
        'titre': f'Profils d\'Acquéreurs - {location}',
        'date_generation': datetime.now().isoformat(),
        'profils_identifies': [
            {
                'nom': 'Jeunes Couples Actifs',
                'pourcentage': 35,
                'age_moyen': '28-35 ans',
                'revenus': '45 000 - 65 000 €',
                'budget_moyen': '280 000 €',
                'preferences': ['2-3 pièces', 'Balcon/terrasse', 'Parking'],
                'canaux_communication': ['Réseaux sociaux', 'Sites immobiliers', 'Bouche-à-oreille']
            },
            {
                'nom': 'Familles Etablies',
                'pourcentage': 28,
                'age_moyen': '35-45 ans',
                'revenus': '60 000 - 85 000 €',
                'budget_moyen': '420 000 €',
                'preferences': ['Maison', 'Jardin', 'Garage', 'Proximité écoles'],
                'canaux_communication': ['Agences traditionnelles', 'Recommandations', 'Presse locale']
            },
            {
                'nom': 'Investisseurs Locatifs',
                'pourcentage': 22,
                'age_moyen': '40-55 ans',
                'revenus': '70 000 - 120 000 €',
                'budget_moyen': '320 000 €',
                'preferences': ['Rendement', 'Proximité transports', 'Facilité gestion'],
                'canaux_communication': ['Réseaux professionnels', 'Événements immobiliers']
            }
        ],
        'strategies_ciblage': [
            'Créer du contenu spécialisé pour chaque profil',
            'Adapter les canaux de communication',
            'Personnaliser les argumentaires de vente',
            'Organiser des événements ciblés'
        ]
    }

def generer_suggestions_contenu(type_contenu, sujet, quartier, mots_cles):
    """Générer des suggestions de contenu (simulation d'IA)"""
    suggestions = []
    
    if type_contenu == 'post_linkedin':
        suggestions = [
            f"🏡 Découvrez les opportunités immobilières exceptionnelles du quartier {quartier} ! {sujet} - Contactez-moi pour une expertise personnalisée. #ImmobilierToulouse #Investissement",
            f"💡 Saviez-vous que {quartier} offre un potentiel de plus-value remarquable ? {sujet} - Parlons de votre projet immobilier ! #ConseilImmobilier #Expertise",
            f"🎯 {sujet} dans le secteur {quartier} : une opportunité à saisir ! Mon expertise locale à votre service. #ImmobilierLocal #Opportunité"
        ]
    elif type_contenu == 'post_facebook':
        suggestions = [
            f"🌟 Vous cherchez à acheter ou vendre dans le quartier {quartier} ? {sujet} Je connais parfaitement ce secteur et ses spécificités. Contactez-moi !",
            f"🏘️ Le marché de {quartier} évolue rapidement ! {sujet} Profitez de mon expertise locale pour optimiser votre projet immobilier.",
            f"💼 {sujet} - Spécialiste du secteur {quartier}, je vous accompagne dans tous vos projets immobiliers avec passion et professionnalisme !"
        ]
    elif type_contenu == 'annonce':
        suggestions = [
            f"Magnifique opportunité dans le quartier prisé de {quartier} ! {sujet} - Bien d'exception alliant charme et modernité.",
            f"Coup de cœur assuré pour ce bien situé à {quartier} ! {sujet} - Idéal pour investisseurs avisés ou famille recherchant la qualité.",
            f"Exclusivité ! {sujet} dans le secteur recherché de {quartier}. Prestations haut de gamme et environnement privilégié."
        ]
    
    return suggestions

def generer_conseils_seo(mots_cles):
    """Générer des conseils SEO (simulation d'IA)"""
    return [
        f"Utilisez les mots-clés '{', '.join(mots_cles[:3])}' dans les 100 premiers mots",
        "Ajoutez des hashtags locaux pour améliorer la visibilité",
        "Incluez un appel à l'action clair",
        "Optimisez pour la recherche mobile",
        "Utilisez des émojis pour augmenter l'engagement"
    ]

def generer_variantes_messages(message_base):
    """Générer des variantes d'un message (simulation d'IA)"""
    if not message_base:
        return []
    
    return [
        message_base.replace('!', '.').replace('🏡', '🏠'),
        message_base.replace('Découvrez', 'Explorez').replace('exceptionnelles', 'uniques'),
        message_base.replace('Contactez-moi', 'Appelez-moi').replace('expertise', 'conseil')
    ]

