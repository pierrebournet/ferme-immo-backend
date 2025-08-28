from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
from datetime import datetime

class Neighborhood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Scores et prédictions
    rotation_rate_score = db.Column(db.Float, default=0.0)  # Score de taux de rotation
    potential_score = db.Column(db.Float, default=0.0)  # Score de potentiel de farming
    demand_indicator = db.Column(db.Float, default=0.0)  # Indicateur de demande
    
    # Données démographiques
    average_age = db.Column(db.Float)
    average_income = db.Column(db.Float)
    population = db.Column(db.Integer)
    
    # Données immobilières
    average_price_m2 = db.Column(db.Float)
    average_sale_time = db.Column(db.Integer)  # en jours
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Neighborhood {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'postal_code': self.postal_code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'rotation_rate_score': self.rotation_rate_score,
            'potential_score': self.potential_score,
            'demand_indicator': self.demand_indicator,
            'average_age': self.average_age,
            'average_income': self.average_income,
            'population': self.population,
            'average_price_m2': self.average_price_m2,
            'average_sale_time': self.average_sale_time,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

