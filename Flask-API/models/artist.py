from db import db
import Notation as n

genres = ('REGGAE', 'POP', 'TRAP', 'HIP HOP', 'ROCK', 'INDIE', 'HEAVY', 'ELECTRONIC', 'OTHER')

class ArtistModel(db.Model):
    __tablename__ = n.ARTS #This is table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique = True, nullable=False)
    country = db.Column(db.String(30), nullable=False)
    genre = db.Column(db.Enum(*genres, name='genres_types'), nullable=False)

    def __init__(self, name, country, genre):
        self.name = name
        self.country = country
        self.genre = genre

    def json(self):
        return {
            n.ART: {
                n.ID: self.id,
                n.NM: self.name,
                n.CTRY: self.country,
                n.GNR: self.genre
            }
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def modify_from_db(self, name, country, genre):
        self.name = name
        self.country = country
        self.genre = genre
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, aid):
        return ArtistModel.query.filter_by(id=aid).first()

    @classmethod
    def find_by_name(cls, aname):
        return ArtistModel.query.filter_by(name=aname).first()

    @classmethod
    def find_by_country(cls, acountry):
        return ArtistModel.query.filter_by(country=acountry).all()

    @classmethod
    def find_by_genre(cls, agenre):
        return ArtistModel.query.filter_by(genre=agenre).all()

    @classmethod
    def return_all(cls):
        return {n.ARTS:
                    [a.json()[n.ART] for a in ArtistModel.query.all()]
               }