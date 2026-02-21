from flask import Blueprint, request, jsonify
from extensions.models import db, Candidat

candidats_bp = Blueprint('candidates', __name__)


# POST /candidates
@candidats_bp.route('/candidates', methods=['POST'])
def create_candidat():

    data = request.json

    # Vérifier body
    if not data:
        return jsonify({"message": "Aucune donnée envoyée"}), 400

    nom = data.get("nom")
    email = data.get("email")
    bio = data.get("bio")
    diplome = data.get("diplome")

    # Vérifier champs obligatoires
    if not nom or not email:
        return jsonify({
            "message": "Nom et email sont obligatoires"
        }), 400

    # Vérifier unicité email (EXIGENCE DU PROF)
    candidat_exist = Candidat.query.filter_by(email=email).first()

    if candidat_exist:
        return jsonify({
            "message": "Email déjà utilisé"
        }), 400

    # Création candidat
    candidat = Candidat(
        nom=nom,
        email=email,
        bio=bio,
        diplome=diplome
    )

    db.session.add(candidat)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Erreur lors de la création",
            "error": str(e)
        }), 500

    return jsonify({
        "message": "Candidat créé avec succès",
        "candidat": {
            "id": candidat.id,
            "nom": candidat.nom,
            "email": candidat.email,
            "bio": candidat.bio,
            "diplome": candidat.diplome
        }
    }), 201
