from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")  #get setup from .env
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    #remove the warning
db = SQLAlchemy(app)