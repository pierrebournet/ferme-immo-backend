from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
from datetime import datetime

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)  # appartement, maison, etc.
    surface = db.Column(db.Float)  # en m²
    rooms = db.Column(db.Integer)
    price = db.Column(db.Float)
    sale_date = db.Column(db.Date)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Property {self.address}>'

    def to_dict(self):
        return {
            'id': self.id,
            'address': self.address,
            'city': self.city,
            'postal_code': self.postal_code,
            'property_type': self.property_type,
            'surface': self.surface,
            'rooms': self.rooms,
            'price': self.price,
            'sale_date': self.sale_date.isoformat() if self.sale_date else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

