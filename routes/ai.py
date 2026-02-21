from flask import Blueprint, request, jsonify
from extensions.models import db, OffreEmploi, Candidat
from services.ai_service import analyze_match

# création blueprint
ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/offers/<int:id>/analyze-match", methods=["POST"])
def analyze_offer_match(id):
    data = request.json

    # Sécurité si le body JSON est vide
    if not data:
        return jsonify({"message": "Le corps de la requête est vide"}), 400

    candidat_id = data.get("candidat_id")

    if not candidat_id:
        return jsonify({
            "message": "candidat_id est requis"
        }), 400

    # récupérer offre (Utilisation de db.session.get pour SQLAlchemy 2.0)
    offre_emploi = db.session.get(OffreEmploi, id)

    if offre_emploi is None:
        return jsonify({
            "message": "Offre non trouvée"
        }), 404

    # récupérer candidat
    candidat = db.session.get(Candidat, candidat_id)

    if candidat is None:
        return jsonify({
            "message": "Candidat non trouvé"
        }), 404

    # appeler le service IA
    # ATTENTION : Les noms des arguments doivent correspondre à ai_service.py
    result = analyze_match(
        description_offre_emploi=offre_emploi.description, # Nom exact de l'argument dans ai_service
        bio_candidat=candidat.bio or ""
    )

    if result is None:
        return jsonify({
            "message": "Erreur lors de l'analyse IA"
        }), 500

    # retourner résultat
    return jsonify({
        "offre_id": offre_emploi.id,
        "candidat_id": candidat.id,
        "score": result.get("score"),
        "justification": result.get("justification")
    }), 200