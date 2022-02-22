import sqlalchemy
from datetime import timedelta

from flask import Flask, Response, request
#from flask_cors import CORS

from Database.config import Config
from Database.database import db, migrate

app = Flask(__name__)
app.config.from_object('database.config.Config')

#CORS(app, supports_credentials=True)

#Add Routes Here

db.init_app(app)
migrate.init_app(app, db, directory="Database/migration")