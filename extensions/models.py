from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, Integer, DateTime, ForeignKey

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

#table des candidats
class Candidat(db.Model):

    #nom reel de la table dans la base de données
    __tablename__ = "candidats"

    #collonnes de la table
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    diplome: Mapped[str] = mapped_column(String(100), nullable=True)

    #un candidat peut avoir plusieurs candidatures
    candidatures: Mapped[list["Candidature"]] = relationship("Candidature", back_populates="candidat")

#table des offres d'emploi
class OffreEmploi(db.Model):
    __tablename__ = "offres_emploi"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titre: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    competences: Mapped[str] = mapped_column(String(200), nullable=True)
    salaire: Mapped[float] = mapped_column(Float, nullable=True)

    #une offre d'emploi peut avoir plusieurs candidatures
    candidatures: Mapped[list["Candidature"]] = relationship("Candidature", back_populates="offre")

#table candidature (table de liaison)
class Candidature(db.Model):
    __tablename__ = "candidatures"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_candidature: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    #clés étrangères
    candidat_id: Mapped[int] = mapped_column(Integer, ForeignKey("candidats.id"), nullable=False)
    offre_emploi_id: Mapped[int] = mapped_column(Integer, ForeignKey("offres_emploi.id"), nullable=False)

    #relations
    candidat: Mapped["Candidat"] = relationship("Candidat", back_populates="candidatures")
    offre: Mapped["OffreEmploi"] = relationship("OffreEmploi", back_populates="candidatures")
    