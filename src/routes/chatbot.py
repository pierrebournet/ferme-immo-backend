from flask import Blueprint, jsonify, request
from src.models.lead import Lead, db
from datetime import datetime
import json
import random

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chatbot/conversation', methods=['POST'])
def handle_conversation():
    """Gérer une conversation avec le chatbot de pré-qualification"""
    data = request.json
    message_utilisateur = data.get('message', '').lower()
    session_id = data.get('session_id')
    contexte = data.get('contexte', {})
    
    # Analyser l'intention du message
    intention = analyser_intention(message_utilisateur)
    
    # Générer la réponse appropriée
    reponse = generer_reponse_chatbot(intention, message_utilisateur, contexte)
    
    # Mettre à jour le contexte de la conversation
    nouveau_contexte = mettre_a_jour_contexte(contexte, intention, message_utilisateur)
    
    # Vérifier si on peut créer un lead
    lead_cree = None
    if peut_creer_lead(nouveau_contexte):
        lead_cree = creer_lead_depuis_contexte(nouveau_contexte)
    
    return jsonify({
        'reponse': reponse,
        'intention': intention,
        'contexte': nouveau_contexte,
        'lead_cree': lead_cree.to_dict() if lead_cree else None,
        'suggestions': generer_suggestions_reponse(intention),
        'prochaine_question': generer_prochaine_question(nouveau_contexte)
    })

@chatbot_bp.route('/chatbot/intentions', methods=['GET'])
def get_available_intentions():
    """Récupérer la liste des intentions disponibles"""
    intentions = [
        {
            'nom': 'salutation',
            'description': 'Saluer le chatbot',
            'exemples': ['bonjour', 'salut', 'hello']
        },
        {
            'nom': 'recherche_achat',
            'description': 'Recherche d\'un bien à acheter',
            'exemples': ['je cherche à acheter', 'je veux acheter une maison']
        },
        {
            'nom': 'recherche_vente',
            'description': 'Vente d\'un bien',
            'exemples': ['je veux vendre', 'vendre ma maison']
        },
        {
            'nom': 'information_budget',
            'description': 'Information sur le budget',
            'exemples': ['mon budget est de', 'je peux payer']
        },
        {
            'nom': 'information_localisation',
            'description': 'Information sur la localisation souhaitée',
            'exemples': ['je cherche à toulouse', 'dans le quartier']
        },
        {
            'nom': 'information_contact',
            'description': 'Fourniture des coordonnées',
            'exemples': ['mon email est', 'mon téléphone']
        },
        {
            'nom': 'question_marche',
            'description': 'Question sur le marché immobilier',
            'exemples': ['comment va le marché', 'les prix augmentent']
        },
        {
            'nom': 'demande_rdv',
            'description': 'Demande de rendez-vous',
            'exemples': ['je veux un rendez-vous', 'pouvons-nous nous rencontrer']
        }
    ]
    
    return jsonify(intentions)

@chatbot_bp.route('/chatbot/conversations', methods=['GET'])
def get_conversations():
    """Récupérer l'historique des conversations"""
    # Dans une vraie implémentation, on stockerait les conversations en base
    # Ici on retourne des données simulées
    conversations = [
        {
            'session_id': 'session_123',
            'date_debut': datetime.now().isoformat(),
            'messages': 5,
            'lead_genere': True,
            'statut': 'qualifie'
        },
        {
            'session_id': 'session_124',
            'date_debut': datetime.now().isoformat(),
            'messages': 3,
            'lead_genere': False,
            'statut': 'en_cours'
        }
    ]
    
    return jsonify(conversations)

def analyser_intention(message):
    """Analyser l'intention d'un message utilisateur (simulation d'IA)"""
    message = message.lower()
    
    # Mots-clés pour chaque intention
    intentions_mots_cles = {
        'salutation': ['bonjour', 'salut', 'hello', 'bonsoir', 'hey'],
        'recherche_achat': ['acheter', 'achat', 'acquérir', 'cherche à acheter', 'veux acheter'],
        'recherche_vente': ['vendre', 'vente', 'céder', 'veux vendre', 'mettre en vente'],
        'information_budget': ['budget', 'prix', 'coût', 'payer', 'financement', 'euros', '€'],
        'information_localisation': ['toulouse', 'quartier', 'secteur', 'zone', 'ville', 'région'],
        'information_contact': ['email', 'téléphone', 'contact', 'joindre', '@', 'appeler'],
        'question_marche': ['marché', 'tendance', 'évolution', 'prix', 'immobilier'],
        'demande_rdv': ['rendez-vous', 'rencontrer', 'rdv', 'voir', 'visiter'],
        'au_revoir': ['au revoir', 'bye', 'à bientôt', 'merci', 'stop']
    }
    
    # Analyser le message
    for intention, mots_cles in intentions_mots_cles.items():
        if any(mot in message for mot in mots_cles):
            return intention
    
    return 'autre'

def generer_reponse_chatbot(intention, message, contexte):
    """Générer une réponse appropriée selon l'intention (simulation d'IA)"""
    reponses = {
        'salutation': [
            "Bonjour ! Je suis l'assistant virtuel de Pierre Bournet, spécialiste immobilier sur Toulouse Sud. Comment puis-je vous aider aujourd'hui ?",
            "Salut ! Ravi de vous rencontrer. Je suis là pour vous accompagner dans votre projet immobilier. Que recherchez-vous ?",
            "Bonjour et bienvenue ! Je peux vous aider à trouver le bien de vos rêves ou à vendre votre propriété. Par quoi commençons-nous ?"
        ],
        'recherche_achat': [
            "Parfait ! Vous souhaitez acheter un bien immobilier. Quel type de bien vous intéresse ? (appartement, maison, terrain...)",
            "Excellente nouvelle ! Pour mieux vous conseiller, pouvez-vous me dire dans quel secteur vous cherchez et votre budget approximatif ?",
            "Super ! Je vais vous aider à trouver le bien idéal. Avez-vous une préférence géographique sur Toulouse Sud ?"
        ],
        'recherche_vente': [
            "Je comprends que vous souhaitez vendre votre bien. Pouvez-vous me donner quelques détails : type de bien, localisation, surface approximative ?",
            "Parfait ! La vente d'un bien nécessite une expertise précise. Dans quel quartier se trouve votre propriété ?",
            "Excellente décision ! Pour une estimation précise, j'aurais besoin de connaître les caractéristiques de votre bien."
        ],
        'information_budget': [
            "Merci pour cette information sur votre budget. Cela m'aide à mieux cibler les biens qui pourraient vous convenir.",
            "Parfait ! Avec ces éléments budgétaires, je peux vous proposer des biens adaptés à vos moyens.",
            "Très bien ! Votre budget est noté. Avez-vous des critères particuliers pour votre futur bien ?"
        ],
        'information_localisation': [
            "Excellent choix de secteur ! Je connais très bien cette zone. Avez-vous des préférences particulières dans ce quartier ?",
            "Parfait ! Ce secteur offre de belles opportunités. Qu'est-ce qui vous attire dans cette zone ?",
            "Très bon choix ! Cette localisation présente de nombreux avantages. Cherchez-vous quelque chose de spécifique ?"
        ],
        'information_contact': [
            "Merci pour vos coordonnées ! Je les transmets immédiatement à Pierre Bournet qui vous contactera rapidement.",
            "Parfait ! Vos informations sont enregistrées. Un expert va vous recontacter sous 24h pour approfondir votre projet.",
            "Excellent ! Avec ces éléments, nous pouvons vous proposer un accompagnement personnalisé."
        ],
        'question_marche': [
            "Le marché immobilier sur Toulouse Sud est dynamique ! Les prix sont en légère hausse (+5% sur 12 mois) avec une demande soutenue.",
            "Excellente question ! Le marché local présente de belles opportunités, notamment pour les familles et les investisseurs.",
            "Le marché évolue positivement ! Souhaitez-vous des informations sur un secteur particulier ?"
        ],
        'demande_rdv': [
            "Bien sûr ! Pierre Bournet sera ravi de vous rencontrer. Laissez-moi vos coordonnées et vos disponibilités.",
            "Parfait ! Un rendez-vous personnalisé est la meilleure façon d'avancer. Quand seriez-vous disponible ?",
            "Excellente idée ! Pour organiser ce rendez-vous, j'ai besoin de votre contact et de vos créneaux préférés."
        ],
        'au_revoir': [
            "Au revoir et merci pour votre visite ! N'hésitez pas à revenir si vous avez d'autres questions.",
            "À bientôt ! Votre projet immobilier nous tient à cœur, revenez quand vous voulez !",
            "Merci et à bientôt ! Pierre Bournet et son équipe restent à votre disposition."
        ],
        'autre': [
            "Je ne suis pas sûr de bien comprendre. Pouvez-vous reformuler votre question ?",
            "Intéressant ! Pouvez-vous m'en dire plus pour que je puisse mieux vous aider ?",
            "Je vois ! Pour mieux vous conseiller, pouvez-vous préciser votre demande ?"
        ]
    }
    
    return random.choice(reponses.get(intention, reponses['autre']))

def mettre_a_jour_contexte(contexte, intention, message):
    """Mettre à jour le contexte de la conversation"""
    nouveau_contexte = contexte.copy()
    
    # Extraire des informations du message selon l'intention
    if intention == 'recherche_achat':
        nouveau_contexte['type_projet'] = 'achat'
    elif intention == 'recherche_vente':
        nouveau_contexte['type_projet'] = 'vente'
    elif intention == 'information_budget':
        # Extraire le budget du message (simulation)
        import re
        budget_match = re.search(r'(\d+(?:\s*\d+)*)\s*(?:euros?|€)', message)
        if budget_match:
            nouveau_contexte['budget'] = budget_match.group(1).replace(' ', '')
    elif intention == 'information_localisation':
        # Extraire la localisation (simulation)
        if 'toulouse' in message:
            nouveau_contexte['localisation'] = 'Toulouse'
        if 'quartier' in message:
            nouveau_contexte['localisation_precise'] = True
    elif intention == 'information_contact':
        # Extraire email/téléphone (simulation)
        import re
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message)
        if email_match:
            nouveau_contexte['email'] = email_match.group()
        
        phone_match = re.search(r'(?:\+33|0)[1-9](?:[0-9]{8})', message.replace(' ', ''))
        if phone_match:
            nouveau_contexte['telephone'] = phone_match.group()
    
    # Incrémenter le compteur de messages
    nouveau_contexte['nb_messages'] = nouveau_contexte.get('nb_messages', 0) + 1
    
    return nouveau_contexte

def peut_creer_lead(contexte):
    """Vérifier si on a assez d'informations pour créer un lead"""
    elements_requis = ['type_projet']
    elements_optionnels = ['budget', 'localisation', 'email', 'telephone']
    
    # Vérifier les éléments requis
    if not all(elem in contexte for elem in elements_requis):
        return False
    
    # Vérifier qu'on a au moins un moyen de contact
    if not any(elem in contexte for elem in ['email', 'telephone']):
        return False
    
    return True

def creer_lead_depuis_contexte(contexte):
    """Créer un lead à partir du contexte de conversation"""
    if not peut_creer_lead(contexte):
        return None
    
    lead = Lead(
        first_name='Prospect',  # À améliorer avec extraction du nom
        last_name='Chatbot',
        email=contexte.get('email', 'prospect@example.com'),
        phone=contexte.get('telephone'),
        lead_type='buyer' if contexte.get('type_projet') == 'achat' else 'seller',
        budget_min=float(contexte.get('budget', 0)) * 0.8 if contexte.get('budget') else None,
        budget_max=float(contexte.get('budget', 0)) * 1.2 if contexte.get('budget') else None,
        location_interest=contexte.get('localisation'),
        source='chatbot',
        notes=f"Lead généré par chatbot. Contexte: {json.dumps(contexte, ensure_ascii=False)}"
    )
    
    # Calculer le score
    from src.routes.lead import calculate_lead_score
    lead.score = calculate_lead_score(lead)
    
    db.session.add(lead)
    db.session.commit()
    
    return lead

def generer_suggestions_reponse(intention):
    """Générer des suggestions de réponse pour l'utilisateur"""
    suggestions = {
        'salutation': [
            "Je cherche à acheter un bien",
            "Je veux vendre ma propriété",
            "J'ai des questions sur le marché"
        ],
        'recherche_achat': [
            "Une maison avec jardin",
            "Un appartement 3 pièces",
            "Dans le centre de Toulouse"
        ],
        'recherche_vente': [
            "Une maison de 120m²",
            "Un appartement T3",
            "Dans le quartier des Minimes"
        ],
        'autre': [
            "Je cherche à acheter",
            "Je veux vendre",
            "Informations sur les prix"
        ]
    }
    
    return suggestions.get(intention, suggestions['autre'])

def generer_prochaine_question(contexte):
    """Générer la prochaine question à poser selon le contexte"""
    if 'type_projet' not in contexte:
        return "Souhaitez-vous acheter ou vendre un bien immobilier ?"
    
    if contexte.get('type_projet') == 'achat':
        if 'budget' not in contexte:
            return "Quel est votre budget approximatif pour cet achat ?"
        if 'localisation' not in contexte:
            return "Dans quel secteur de Toulouse Sud recherchez-vous ?"
        if 'email' not in contexte and 'telephone' not in contexte:
            return "Pouvez-vous me laisser votre email ou téléphone pour que Pierre vous recontacte ?"
    
    elif contexte.get('type_projet') == 'vente':
        if 'localisation' not in contexte:
            return "Dans quel quartier se trouve votre bien à vendre ?"
        if 'email' not in contexte and 'telephone' not in contexte:
            return "Comment Pierre peut-il vous contacter pour une estimation gratuite ?"
    
    return "Avez-vous d'autres questions sur votre projet immobilier ?"

