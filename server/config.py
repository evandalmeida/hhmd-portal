import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.secret_key = b'u\xd2\xdc\xe82\xa3\xc0\xca\xe7H\xd03oi\xd1\x95\xcc\x7f'


app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

db = SQLAlchemy(metadata=metadata)
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

bcrypt = Bcrypt()


