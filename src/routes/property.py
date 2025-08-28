from flask import Blueprint, jsonify, request
from src.models.property import Property, db
from datetime import datetime

property_bp = Blueprint('property', __name__)

@property_bp.route('/properties', methods=['GET'])
def get_properties():
    """Récupérer toutes les propriétés avec filtres optionnels"""
    city = request.args.get('city')
    property_type = request.args.get('property_type')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    query = Property.query
    
    if city:
        query = query.filter(Property.city.ilike(f'%{city}%'))
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if min_price:
        query = query.filter(Property.price >= min_price)
    if max_price:
        query = query.filter(Property.price <= max_price)
    
    properties = query.all()
    return jsonify([prop.to_dict() for prop in properties])

@property_bp.route('/properties', methods=['POST'])
def create_property():
    """Créer une nouvelle propriété"""
    data = request.json
    
    # Conversion de la date de vente si fournie
    sale_date = None
    if data.get('sale_date'):
        sale_date = datetime.fromisoformat(data['sale_date']).date()
    
    property_obj = Property(
        address=data['address'],
        city=data['city'],
        postal_code=data['postal_code'],
        property_type=data['property_type'],
        surface=data.get('surface'),
        rooms=data.get('rooms'),
        price=data.get('price'),
        sale_date=sale_date,
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )
    
    db.session.add(property_obj)
    db.session.commit()
    return jsonify(property_obj.to_dict()), 201

@property_bp.route('/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    """Récupérer une propriété par son ID"""
    property_obj = Property.query.get_or_404(property_id)
    return jsonify(property_obj.to_dict())

@property_bp.route('/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    """Mettre à jour une propriété"""
    property_obj = Property.query.get_or_404(property_id)
    data = request.json
    
    property_obj.address = data.get('address', property_obj.address)
    property_obj.city = data.get('city', property_obj.city)
    property_obj.postal_code = data.get('postal_code', property_obj.postal_code)
    property_obj.property_type = data.get('property_type', property_obj.property_type)
    property_obj.surface = data.get('surface', property_obj.surface)
    property_obj.rooms = data.get('rooms', property_obj.rooms)
    property_obj.price = data.get('price', property_obj.price)
    property_obj.latitude = data.get('latitude', property_obj.latitude)
    property_obj.longitude = data.get('longitude', property_obj.longitude)
    
    if data.get('sale_date'):
        property_obj.sale_date = datetime.fromisoformat(data['sale_date']).date()
    
    db.session.commit()
    return jsonify(property_obj.to_dict())

@property_bp.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    """Supprimer une propriété"""
    property_obj = Property.query.get_or_404(property_id)
    db.session.delete(property_obj)
    db.session.commit()
    return '', 204

@property_bp.route('/properties/stats', methods=['GET'])
def get_property_stats():
    """Obtenir des statistiques sur les propriétés"""
    city = request.args.get('city')
    
    query = Property.query
    if city:
        query = query.filter(Property.city.ilike(f'%{city}%'))
    
    properties = query.all()
    
    if not properties:
        return jsonify({
            'total_properties': 0,
            'average_price': 0,
            'average_price_m2': 0,
            'property_types': {}
        })
    
    total_properties = len(properties)
    prices = [p.price for p in properties if p.price]
    surfaces = [p.surface for p in properties if p.surface]
    
    average_price = sum(prices) / len(prices) if prices else 0
    average_price_m2 = sum([p.price / p.surface for p in properties if p.price and p.surface]) / len([p for p in properties if p.price and p.surface]) if any(p.price and p.surface for p in properties) else 0
    
    # Comptage des types de propriétés
    property_types = {}
    for prop in properties:
        property_types[prop.property_type] = property_types.get(prop.property_type, 0) + 1
    
    return jsonify({
        'total_properties': total_properties,
        'average_price': round(average_price, 2),
        'average_price_m2': round(average_price_m2, 2),
        'property_types': property_types
    })

