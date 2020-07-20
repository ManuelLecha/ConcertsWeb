from flask import Flask
from flask_restful import  Api
from flask_cors import CORS
from resources.artists import Artist, ArtistList
from resources.events import Event, EventList, EventArtistsList
from resources.event_artist import EventArtist, ArtistEventsList
from resources.orders import Orders, OrdersList
from resources.login import Login
from resources.accounts import AccountsList, Account
from db import db
from flask_migrate import Migrate
from flask import render_template
from decouple import config as config_decouple
from config import config

app = Flask(__name__)
environment = config['development']
if config_decouple('PRODUCTION', cast=bool, default=False):
    environment = config['production']

app.config.from_object(environment)
migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def render_vue():
    return render_template("index.html")


#ARTIST
api.add_resource(Artist, '/artist/<int:id>', '/artist')

#ARTIST LIST
api.add_resource(ArtistList, '/artists')

#EVENT
api.add_resource(Event, '/event/<int:id>', '/event')

#EVENT LIST
api.add_resource(EventList, '/events')

#EVENT ARTIST LIST
api.add_resource(EventArtistsList, '/event/<int:id>/artists')

#EVENT ARTIST
api.add_resource(EventArtist, '/event/<int:id_event>/artist/<int:id_artist>', '/event/<int:id_event>/artist')

#ARTIST EVENT LIST
api.add_resource(ArtistEventsList, '/artist/<int:id>/events')

#ORDER
api.add_resource(Orders, '/orders/<string:username>')

#ORDER LIST
api.add_resource(OrdersList, '/orders')

#ACCOUNT
api.add_resource(Account, '/account', '/account/<string:username>')

#ACCOUNTS LIST
api.add_resource(AccountsList, '/accounts')

#LOGIN
api.add_resource(Login, '/login')


if __name__ == '__main__':
    app.run(port=5000, debug=True)  # This command should be modified before deploying our application
