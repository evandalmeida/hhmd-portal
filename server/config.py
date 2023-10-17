from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# SQLAlchemy metadata with naming convention
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

# Initialize SQLAlchemy with metadata
db = SQLAlchemy(metadata=metadata)
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize Flask-RESTful
api = Api(app)

# Configure CORS for specific resources
cors = CORS(
    app,
    resources={
        r'/api/*': {
            'origins': 'http://localhost:3000',
            'methods': ['GET', 'POST', 'DELETE']
        }
    }
)