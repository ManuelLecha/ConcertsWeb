from models.accounts import AccountsModel
from flask_restful import Resource, reqparse
import Notation as n
from lock import lock


class Account(Resource):

    def get(self, username):
        user = AccountsModel.find_by_username(username)
        if user:
            return user.json(), 200
        else:
            return {n.MSG: "User not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()  # create parameters parser from request
        # define al input parameters need and its type
        parser.add_argument(n.USR, type=str, required=True, help="Username")
        parser.add_argument(n.PSW, type=str, required=True, help="Password")
        data = parser.parse_args()

        with lock.lock:
            user = AccountsModel.find_by_username(data[n.USR])
            if user:
                return {n.MSG: "User already in database"}, 400

            user = AccountsModel(data[n.USR])
            user.hash_password(data[n.PSW])
            user.save_to_db()
            return user.json(), 200

    def delete(self, username):
        with lock.lock:
            user = AccountsModel.find_by_username(username)
            if user:
                user.delete_from_db()
                return {n.MSG: "User deleted successfully"}, 200
            else:
                return {n.MSG: "User not found"}, 404


class AccountsList(Resource):

    def get(self):
        return AccountsModel.return_all(), 200