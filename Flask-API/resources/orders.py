from models.event import EventModel
from models.orders import OrdersModel
from models.accounts import AccountsModel, auth
from flask_restful import Resource, reqparse
from flask import g
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import Notation as n
from db import db
from lock import lock


class Orders (Resource):

    def get(self, username):
        account = AccountsModel.find_by_username(username)
        if account:
            return {n.ORDRS: account.orders}, 200
        else:
            return {n.MSG: "Username not found"}, 404

    @auth.login_required(role='user')
    def post(self, username):
        user = AccountsModel.find_by_username(username)
        if user:
            parser = reqparse.RequestParser()
            parser.add_argument(n.IDEVNT, type=int, required=True, help="Id of the event")
            parser.add_argument(n.TCK, type=int, required=True, help="Number of tickets the user wants to buy")
            data = parser.parse_args()

            with lock.lock:
                if username == g.user.username:
                    event = EventModel.find_by_id(data[n.IDEVNT])
                    if event:
                        price = event.price*data[n.TCK]
                        if user.available_money >= price:
                            if event.total_available_tickets >= data[n.TCK]:
                                try:
                                    user.pay(price)
                                    event.sell(data[n.TCK])
                                    new_order = OrdersModel(data[n.IDEVNT], data[n.TCK])
                                    user.orders.append(new_order)
                                    new_order.save_to_db()
                                    user.save_to_db()
                                    event.save_to_db()
                                    return new_order.json(), 201
                                except:
                                    return {n.MSG: "Error Description"}, 500
                            else:
                                return {n.MSG: "The event does not have enough available ticket"}, 400
                        else:
                            return {n.MSG: "The user does not have enough money"}, 400
                    else:
                        return {n.MSG: "Event not found"}, 404
                else:
                    return {n.MSG: "Username error"}, 400
        else:
            return {n.MSG: "Username not found"}, 404


class OrdersList(Resource):

    def get(self):
        return OrdersModel.return_all(), 200