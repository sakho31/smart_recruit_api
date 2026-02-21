from flask import Blueprint, request, jsonify
from extensions.models import db, OffreEmploi

offres_emploi_bp = Blueprint('offres_emploi', __name__)


# POST /offers
@offres_emploi_bp.route('/offers', methods=['POST'])
def create_offre():

    data = request.json

    # Vérifier que le body existe
    if not data:
        return jsonify({"message": "Aucune donnée envoyée"}), 400

    titre = data.get("titre")
    description = data.get("description")
    competences = data.get("competences")
    salaire = data.get("salaire")

    # Vérifier champs obligatoires
    if not titre or not description:
        return jsonify({
            "message": "Le titre et la description sont obligatoires"
        }), 400

    # Création de l'offre
    offre = OffreEmploi(
        titre=titre,
        description=description,
        competences=competences,
        salaire=salaire
    )

    db.session.add(offre)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Erreur lors de la création",
            "error": str(e)
        }), 500

    return jsonify({
        "message": "Offre créée avec succès",
        "offre": {
            "id": offre.id,
            "titre": offre.titre,
            "description": offre.description,
            "competences": offre.competences,
            "salaire": offre.salaire
        }
    }), 201
