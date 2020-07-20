from models.accounts import AccountsModel
from flask_restful import Resource, reqparse
import Notation as n
from lock import lock


class Login(Resource):

    def post(self):
        parser = reqparse.RequestParser()  # create parameters parser from request
        # define al input parameters need and its type
        parser.add_argument(n.USR, type=str, required=True, help="Username")
        parser.add_argument(n.PSW, type=str, required=True, help="Password")
        data = parser.parse_args()

        user = AccountsModel.find_by_username(data[n.USR])
        if user:
            verification = user.check_password(data[n.PSW])

            if verification:
                return {n.TKN: user.generate_auth_token().decode('utf-8')}, 200
            else:
                return {n.MSG: "Invalid password"}, 400
        else:
            return {n.MSG: "User not found"}, 404
