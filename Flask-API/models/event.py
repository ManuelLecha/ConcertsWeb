from db import db
import Notation as n

artists_in_event = db.Table('events_artist', db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
                   db.Column('artist_id', db.Integer, db.ForeignKey('artists.id')))

class EventModel(db.Model):
    __tablename__ = n.EVNTS #This is table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    place = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    total_available_tickets = db.Column(db.Integer, nullable=False)
    artists = db.relationship('ArtistModel', secondary=artists_in_event, backref=db.backref(n.EVNTS, lazy='dynamic'))

    __table_args__ = (db.UniqueConstraint(n.NM, n.DATE, n.CTY),)

    def __init__(self, name, place, city, date, price, total_available_tickets):
        self.name = name
        self.place = place
        self.city = city
        self.date = date
        self.price = price
        self.total_available_tickets = total_available_tickets

    def json(self):
        return {
            n.EVNT: {
                n.ID: self.id,
                n.NM: self.name,
                n.PLC: self.place,
                n.CTY: self.city,
                n.DATE: self.date,
                n.ARTS: [a.json()[n.ART] for a in self.artists],
                n.PRC: self.price,
                n.TAT: self.total_available_tickets
            }
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def modify_from_db(self, name, place, city, date, price, total_available_tickets):
        self.name = name
        self.place = place
        self.city = city
        self.date = date
        self.price = price
        self.total_available_tickets = total_available_tickets
        db.session.add(self)
        db.session.commit()

    def sell(self, number_of_tickets):
        self.total_available_tickets = self.total_available_tickets - number_of_tickets


    def get_artists(self):
        return {n.ARTS: [a.json()[n.ART] for a in self.artists]}

    @classmethod
    def find_by_id(cls, eid):
        return EventModel.query.filter_by(id=eid).first()

    @classmethod
    def find_by_name(cls, ename):
        return EventModel.query.filter_by(name=ename).all()

    @classmethod
    def find_by_place(cls, eplace):
        return EventModel.query.filter_by(place=eplace).all()

    @classmethod
    def find_by_city(cls, ecity):
        return EventModel.query.filter_by(city=ecity).all()

    @classmethod
    def find_by_date(cls, edate):
        return EventModel.query.filter_by(date=edate).all()

    @classmethod
    def find_by_artist(cls, eartist_name):
        return EventModel.query.filter(EventModel.artists.any(name=eartist_name)).all()

    @classmethod
    def find_by_uniqueness(cls, ename, edate, ecity):
        return EventModel.query.filter_by(name=ename, date=edate, city=ecity).first()

    @classmethod
    def return_all(cls):
        return {n.EVNTS:
                    [e.json()[n.EVNT] for e in EventModel.query.all()]
               }