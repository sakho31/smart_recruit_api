from config import Config
from flask import Flask, jsonify
from extensions.models import db
from extensions.migrations import migrate
from extensions.schemas import ma
from routes.candidats import candidats_bp
from routes.offres_emploi import offres_emploi_bp
from routes.candidatures import candidatures_bp
from routes.ai import ai_bp


# création de l'application Flask
app = Flask(__name__)

# chargement de la configuration depuis config.py
app.config.from_object(Config)

# initialisation des extensions
db.init_app(app)
migrate.init_app(app, db)
ma.init_app(app)


# enregistrement des blueprints
app.register_blueprint(candidats_bp)
app.register_blueprint(offres_emploi_bp)
app.register_blueprint(candidatures_bp)
app.register_blueprint(ai_bp)

@app.route("/")
def index():
    return jsonify({"message": "Smart Recruit API fonctionne correctement"})


# gestion erreur 404
@app.errorhandler(404)
def not_found_handler(error):
    return jsonify({"status": 404, "message": str(error)}), 404

# gestion erreur 500
@app.errorhandler(500)
def internal_error_handler(error):
    return jsonify({"status": 500, "message": "Une erreur interne est survenue"}), 500

# gestion erreur 503
@app.errorhandler(503)
def service_unavailable_handler(error):
    return jsonify({"status": 503, "message": "Service temporairement indisponible"}), 503


# lancement du serveur
if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)