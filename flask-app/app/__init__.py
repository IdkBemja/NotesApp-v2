from flask import Flask, Blueprint
from flask_cors import CORS
import os 

from app.services.database import init_db


clave = os.urandom(24)
session = init_db()

app = Flask(__name__)
CORS(app, supports_credentials=True)

admin_assets = Blueprint(
    "admin_assets",
    __name__,
    static_folder="../../slim-app/api/assets", 
    static_url_path="/api/admin/assets" 
)



app.register_blueprint(admin_assets)
app.secret_key = clave