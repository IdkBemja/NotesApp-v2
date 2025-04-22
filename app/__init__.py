from flask import Flask
import os 

from app.services.database import init_db


clave = os.urandom(24)


session = init_db()

app = Flask(__name__)

app.secret_key = clave