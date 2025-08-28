import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.property import property_bp
from src.routes.lead import lead_bp
from src.routes.neighborhood import neighborhood_bp
from src.routes.report import report_bp
from src.routes.chatbot import chatbot_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'ferme-immo-saas-secret-key-2024'

# Activer CORS pour permettre les requêtes cross-origin
CORS(app)

# Enregistrer tous les blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(property_bp, url_prefix='/api')
app.register_blueprint(lead_bp, url_prefix='/api')
app.register_blueprint(neighborhood_bp, url_prefix='/api')
app.register_blueprint(report_bp, url_prefix='/api')
app.register_blueprint(chatbot_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Importer tous les modèles pour la création des tables
from src.models.property import Property
from src.models.lead import Lead
from src.models.neighborhood import Neighborhood
from src.models.report import Report

with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
