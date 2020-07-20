from models.artist import ArtistModel, genres
from models.accounts import auth
from flask_restful import Resource,reqparse
import Notation as n
from lock import lock


class Artist(Resource):

    def get(self, id):
        artist = ArtistModel.find_by_id(id)
        if artist:
            return artist.json(), 200
        else:
            return {n.MSG: "Artist not found"}, 404

    @auth.login_required(role='admin')
    def post(self):

        parser = reqparse.RequestParser()  # create parameters parser from request
        # define al input parameters need and its type
        parser.add_argument(n.NM, type=str, required=True, help="Artistic name of the artist")
        parser.add_argument(n.CTRY, type=str, required=True, help="Country nationality of the artist")
        parser.add_argument(n.GNR, type=str, required=True, help="Main genre of the artist")
        data = parser.parse_args()

        with lock.lock:
            if ArtistModel.find_by_name(data[n.NM]):
                return {n.MSG: "Artist already in the data base"}, 409

            if data[n.GNR] not in genres:
                return {n.MSG: "Genre not allowed"}, 400

            try:
                new_artist = ArtistModel(data[n.NM], data[n.CTRY], data[n.GNR])
                new_artist.save_to_db()
                return new_artist.json(), 201
            except:
                return {n.MSG: "Error Description"}, 500

    @auth.login_required(role='admin')
    def delete(self, id):
        with lock.lock:
            artist = ArtistModel.find_by_id(id)
            if artist:
                artist.delete_from_db()
                return {n.MSG: "Artist deleted successfully"}, 200
            else:
                return {n.MSG: "Artist not found"}, 404

    @auth.login_required(role='admin')
    def put(self, id):

        artist = ArtistModel.find_by_id(id)

        if artist:
            parser = reqparse.RequestParser()  # create parameters parser from request
            # define al input parameters need and its type
            parser.add_argument(n.NM, type=str, required=True, help="Artistic name of the artist")
            parser.add_argument(n.CTRY, type=str, required=True, help="Country nationality of the artist")
            parser.add_argument(n.GNR, type=str, required=True, help="Main genre of the artist")
            data = parser.parse_args()

            with lock.lock:
                if data[n.GNR] not in genres:
                    return {n.MSG: "Genre not allowed"}, 400

                aux_artist = ArtistModel.find_by_name(data[n.NM])
                if aux_artist and aux_artist.id != id:
                    return {n.MSG: "Artist already in the data base with another ID"}, 409

                try:
                    artist.modify_from_db(data[n.NM], data[n.CTRY], data[n.GNR])
                    return artist.json(), 200
                except:
                    return {n.MSG: "Error Description"}, 500

        else:
            return {n.MSG: "Artist not found"}, 404

class ArtistList(Resource):

    def get(self):
        return ArtistModel.return_all(), 200