import jwt

from flask import render_template as page
from app import app, user_controller
from app.services.database import BlacklistedToken, session

from flask import request, jsonify
from datetime import datetime, timedelta

@app.route("/")
def index():
    return page("app.html")

# JWT Usage
def is_token_blacklisted(token):
    blacklisted = session.query(BlacklistedToken).filter_by(token=token).first()
    return blacklisted is not None

@app.route("/protected", methods=["GET"])
def protected():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token no proporcionado."}), 401

    try:
        token = token.split(" ")[1]

        if is_token_blacklisted(token):
            return jsonify({"message": "Token inválido o revocado."}), 401

        payload = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        return jsonify({"message": "Acceso permitido.", "user_id": payload["user_id"]}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "El token ha expirado."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido."}), 401
    
@app.route("/refresh-token", methods=["POST"])
def refresh_token():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token no proporcionado."}), 401

    try:
        token = token.split(" ")[1]
        payload = jwt.decode(token, app.secret_key, algorithms=["HS256"], options={"verify_exp": False})

        # Verificar si el token está cerca de expirar
        exp_time = datetime.utcfromtimestamp(payload["exp"])
        if (exp_time - datetime.utcnow()).total_seconds() < 600:  # 10 minutos
            
            # Generarción de un nuevo token
            new_token = user_controller.generate_token(payload["user_id"])
            return jsonify({"token": new_token}), 200

        return jsonify({"message": "El token aún es válido."}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "El token ha expirado. Por favor, inicia sesión nuevamente."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido."}), 401