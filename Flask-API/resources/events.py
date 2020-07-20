from models.event import EventModel
from models.accounts import auth
from flask_restful import Resource,reqparse
import Notation as n
from lock import lock


class Event(Resource):

    def get(self, id):
        event = EventModel.find_by_id(id)
        if event:
            return event.json(), 200
        else:
            return {n.MSG: "Event not found"}, 404

    @auth.login_required(role='admin')
    def post(self):

        parser = reqparse.RequestParser()  # create parameters parser from request
        # define al input parameters need and its type
        parser.add_argument(n.NM, type=str, required=True, help="Name of the event")
        parser.add_argument(n.PLC, type=str, required=True, help="Place or area where the event takes place")
        parser.add_argument(n.CTY, type=str, required=True, help="City that holds the event")
        parser.add_argument(n.DATE, type=str, required=True, help="Date when the event takes place")
        parser.add_argument(n.PRC, type=int, required=True, help="Weighted average price of the event")
        parser.add_argument(n.TAT, type=int, required=True, help="Number of people that can attend the event")
        data = parser.parse_args()

        with lock.lock:
            if EventModel.find_by_uniqueness(data[n.NM], data[n.DATE], data[n.CTY]):
                return {n.MSG: "Event already in the data base"}, 409

            if data[n.PRC] < 0:
                return {n.MSG: "Negative price not allowed"}, 400

            if data[n.TAT] < 0:
                return {n.MSG: "Negative number of tickets not possible"}, 400

            try:
                new_event = EventModel(data[n.NM], data[n.PLC], data[n.CTY], data[n.DATE], data[n.PRC], data[n.TAT])
                new_event.save_to_db()
                return new_event.json(), 201
            except:
                return {n.MSG: "Error Description"}, 500

    @auth.login_required(role='admin')
    def delete(self, id):
        with lock.lock:
            event = EventModel.find_by_id(id)
            if event:
                event.delete_from_db()
                return {n.MSG: "Event deleted successfully"}, 200
            else:
                return {n.MSG: "Event not found"}, 404

    @auth.login_required(role='admin')
    def put(self, id):
        event = EventModel.find_by_id(id)
        if event:
            parser = reqparse.RequestParser()  # create parameters parser from request
            # define al input parameters need and its type
            parser.add_argument(n.NM, type=str, required=True, help="Name of the event")
            parser.add_argument(n.PLC, type=str, required=True, help="Place or area where the event takes place")
            parser.add_argument(n.CTY, type=str, required=True, help="City that holds the event")
            parser.add_argument(n.DATE, type=str, required=True, help="Date when the event takes place")
            parser.add_argument(n.PRC, type=int, required=True, help="Weighted average price of the event")
            parser.add_argument(n.TAT, type=int, required=True, help="Number of people that can attend the event")
            data = parser.parse_args()

            with lock.lock:
                if data[n.PRC] < 0:
                    return {n.MSG: "Negative price not allowed"}, 400

                if data[n.TAT] < 0:
                    return {n.MSG: "Negative number of tickets not possible"}, 400

                aux_event = EventModel.find_by_uniqueness(data[n.NM], data[n.DATE], data[n.CTY])
                if aux_event and aux_event.id != id:
                    return {n.MSG: "Event already in the data base with another ID"}, 409

                try:
                    event.modify_from_db(data[n.NM], data[n.PLC], data[n.CTY], data[n.DATE], data[n.PRC], data[n.TAT])
                    return event.json(), 200
                except:
                    return {n.MSG: "Error Description"}, 500

        else:
            return {n.MSG: "Event not found"}, 404


class EventList(Resource):

    def get(self):
        return EventModel.return_all(), 200



class EventArtistsList(Resource):

    def get(self, id):
        event = EventModel.find_by_id(id)
        if event:
            return event.get_artists(), 200
        else:
            return {n.MSG: "Event not found"}, 404


