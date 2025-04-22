from flask import request, jsonify

from app import app
from app.services.database import User, session
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)