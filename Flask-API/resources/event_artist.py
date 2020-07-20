from models.event import EventModel
from models.artist import ArtistModel
from models.accounts import auth
from flask_restful import Resource,reqparse
import Notation as n
from lock import lock


class EventArtist(Resource):

    def get(self, id_event, id_artist):
        artist = ArtistModel.query.join(ArtistModel.events).filter(EventModel.id == id_event).filter(ArtistModel.id == id_artist).first()
        if not artist:
            return {n.MSG: "Artist or event not found"}, 404
        return artist.json()

    @auth.login_required(role='admin')
    def post(self, id_event):
        event = EventModel.find_by_id(id_event)

        if event:

            parser = reqparse.RequestParser()  # create parameters parser from request
            # define al input parameters need and its type
            parser.add_argument(n.NM, type=str, required=True, help="Artistic name of the artist")
            parser.add_argument(n.CTRY, type=str, required=True, help="Country nationality of the artist")
            parser.add_argument(n.GNR, type=str, required=True, help="Main genre of the artist")
            data = parser.parse_args()

            with lock.lock:
                artist = ArtistModel.find_by_name(data[n.NM])

                if artist and artist.country == data[n.CTRY] and artist.genre == data[n.GNR]:
                    event.artists.append(artist)
                    event.save_to_db()
                    return event.json(), 200
                else:
                    return {n.MSG: "Artist not found"}, 409

        else:
            return {n.MSG: "Event not found"}, 404

    @auth.login_required(role='admin')
    def delete(self, id_event, id_artist):
        with lock.lock:
            event = EventModel.find_by_id(id_event)
            artist = ArtistModel.query.join(ArtistModel.events).filter(EventModel.id == id_event).filter(ArtistModel.id == id_artist).first()

            if artist:
                event.artists.remove(artist)
                return {n.MSG: "Artist deleted successfully"}, 200
            else:
                return {n.MSG: "Artist or event not found"}, 404



class ArtistEventsList(Resource):

    def get(self, id):
        artist = ArtistModel.find_by_id(id)
        if artist:
            return {n.EVNTS: [event.json()[n.EVNT] for event in EventModel.query.filter(EventModel.artists.any(id=id)).all()]}, 200
        else:
            return {n.MSG: "Artist not found"}, 404