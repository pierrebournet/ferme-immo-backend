from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
from datetime import datetime

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # 'market_analysis', 'neighborhood_prediction', etc.
    location = db.Column(db.String(200))  # Zone géographique du rapport
    content = db.Column(db.Text)  # Contenu du rapport en JSON ou HTML
    file_path = db.Column(db.String(500))  # Chemin vers le fichier PDF généré
    status = db.Column(db.String(20), default='generating')  # generating, completed, error
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Report {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'report_type': self.report_type,
            'location': self.location,
            'content': self.content,
            'file_path': self.file_path,
            'status': self.status,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

