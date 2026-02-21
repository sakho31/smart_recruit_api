from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow.exceptions import ValidationError


# initialisation Marshmallow
ma = Marshmallow()

def validate_email(value: str):
    if "@" not in value or "." not in value:
        raise ValidationError("Adresse email invalide")
    
#Schemas d'entité pour la validation et la sérialisation

class CandidatInSchema(ma.Schema):
    nom = fields.Str(required=True)
    email = fields.Email(required=True, validate=validate_email)
    bio = fields.Str()
    diplome = fields.Str()


#Schema de sortie pour les candidats
class CandidatOutSchema(ma.Schema):
    id = fields.Int()
    nom = fields.Str()
    email = fields.Email()
    bio = fields.Str()
    diplome = fields.Str()


class OffreEmploiInSchema(ma.Schema):
    titre = fields.Str(required=True)
    description = fields.Str(required=True)
    competences = fields.Str()
    salaire = fields.Float()

class OffreEmploiOutSchema(ma.Schema):
    id = fields.Int()
    titre = fields.Str()
    description = fields.Str()
    competences = fields.Str()
    salaire = fields.Float()

class CandidatureInSchema(ma.Schema):
    candidat_id = fields.Int(required=True)
    offre_emploi_id = fields.Int(required=True)

class CandidatureOutSchema(ma.Schema):
    id = fields.Int()
    date_candidature = fields.DateTime()
    candidat_id = fields.Int()
    offre_emploi_id = fields.Int()


#instances des schemas
candidat_in_schema = CandidatInSchema()
candidat_out_schema = CandidatOutSchema()
candidats_out_schema = CandidatOutSchema(many=True)

offre_emploi_in_schema = OffreEmploiInSchema()
offre_emploi_out_schema = OffreEmploiOutSchema()
offres_emploi_out_schema = OffreEmploiOutSchema(many=True)

candidature_in_schema = CandidatureInSchema()
candidature_out_schema = CandidatureOutSchema()
candidatures_out_schema = CandidatureOutSchema(many=True)

