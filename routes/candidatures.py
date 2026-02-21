from flask import Blueprint, request, jsonify
from extensions.models import db, Candidat, OffreEmploi, Candidature

candidatures_bp = Blueprint('candidatures', __name__)

@candidatures_bp.route('/apply', methods=['POST'])
def apply():

    data = request.json

    candidat_id = data.get("candidat_id")
    offre_emploi_id = data.get("offre_id")

    candidat = Candidat.query.get(candidat_id)
    offre = OffreEmploi.query.get(offre_emploi_id)

    # Vérifier existence
    if candidat is None or offre is None:
        return jsonify({"message": "Candidat ou offre non trouvé"}), 404

    # Vérifier si candidature existe déjà
    exist = Candidature.query.filter_by(
        candidat_id=candidat_id,
        offre_emploi_id=offre_emploi_id
    ).first()

    if exist:
        return jsonify({"message": "Déjà candidat à cette offre"}), 400

    candidature = Candidature(
        candidat_id=candidat_id,
        offre_emploi_id=offre_emploi_id
    )

    db.session.add(candidature)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Erreur candidature"}), 500

    return jsonify({"message": "Candidature envoyée"}), 201


@candidatures_bp.route('/offers/<int:id>/candidates', methods=['GET'])
def candidates_by_offer(id):

    offre = OffreEmploi.query.get(id)

    if offre is None:
        return jsonify({"message": "Offre non trouvée"}), 404

    candidats = []

    for candidature in offre.candidatures:

        candidat = candidature.candidat

        candidats.append({
            "id": candidat.id,
            "nom": candidat.nom,
            "email": candidat.email,
            "diplome": candidat.diplome
        })

    return jsonify(candidats), 200
