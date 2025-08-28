from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
from datetime import datetime

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    lead_type = db.Column(db.String(20), nullable=False)  # 'buyer' ou 'seller'
    budget_min = db.Column(db.Float)
    budget_max = db.Column(db.Float)
    property_type_interest = db.Column(db.String(100))  # Type de bien recherché
    location_interest = db.Column(db.String(200))  # Zone géographique d'intérêt
    score = db.Column(db.Float, default=0.0)  # Score de "chaleur" du lead
    status = db.Column(db.String(20), default='new')  # new, contacted, qualified, converted, lost
    source = db.Column(db.String(50))  # Source du lead (site web, réseaux sociaux, etc.)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contact_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Lead {self.first_name} {self.last_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'lead_type': self.lead_type,
            'budget_min': self.budget_min,
            'budget_max': self.budget_max,
            'property_type_interest': self.property_type_interest,
            'location_interest': self.location_interest,
            'score': self.score,
            'status': self.status,
            'source': self.source,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_contact_date': self.last_contact_date.isoformat() if self.last_contact_date else None
        }

