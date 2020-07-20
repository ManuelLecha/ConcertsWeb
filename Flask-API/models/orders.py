from db import db
from models.event import EventModel
import Notation as n


class OrdersModel(db.Model):

    __tablename__ = n.ORDRS

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('accounts.username'), nullable=False)
    id_event = db.Column(db.Integer, nullable=False)
    tickets_bought = db.Column(db.Integer, nullable=False)

    def __init__(self, id_event, tickets_bought):
        self.id_event = id_event
        self.tickets_bought = tickets_bought

    def json(self):

        event = EventModel.find_by_id(self.id_event).json()[n.EVNT]

        return {
            n.ORDR: {
                n.ID: self.id,
                n.USR: self.username,
                n.EVNTNM: event[n.NM],
                n.EVNTDT: event[n.DATE],
                n.EVNTCTY: event[n.CTY],
                n.TCK: self.tickets_bought,
            }
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        return {n.ORDRS:
                    [o.json()[n.ORDR] for o in OrdersModel.query.all()]
                }


