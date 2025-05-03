from flask import Flask
from flask_cors import CORS
import os 

from app.services.database import init_db


clave = os.urandom(24)
session = init_db()

app = Flask(__name__)
CORS(app)

app.secret_key = clave