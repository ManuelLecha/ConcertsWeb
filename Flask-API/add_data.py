from models.event import EventModel
from models.artist import ArtistModel
from models.accounts import AccountsModel
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

new_artist1 = ArtistModel('Oques Grasses', 'Spain', 'REGGAE')
db.session.add(new_artist1)

new_artist2 = ArtistModel('Txarango', 'Spain', 'POP')
db.session.add(new_artist2)

new_artist3 = ArtistModel('Bad Gyal', 'Spain', 'TRAP')
db.session.add(new_artist3)

new_artist4 = ArtistModel('Billie Eilish', 'USA', 'INDIE')
db.session.add(new_artist4)

new_event1 = EventModel('Festival Cruilla 2020', 'Parc del Forum', 'Barcelona', '2020-07-03', 60, 15000)
new_event1.artists.append(new_artist1)
new_event1.artists.append(new_artist2)
db.session.add(new_event1)

new_event2 = EventModel('Canet Rock 2020', 'Canet de Mar Beach', 'Barcelona', '2020-07-05', 45, 35000)
new_event2.artists.append(new_artist1)
new_event2.artists.append(new_artist4)
db.session.add(new_event2)

new_user1 = AccountsModel(username='user')
new_user1.hash_password('1234')
db.session.add(new_user1)

new_user1 = AccountsModel(username='admin', is_admin=1)
new_user1.hash_password('admin')
db.session.add(new_user1)

db.session.commit()
db.session.close()