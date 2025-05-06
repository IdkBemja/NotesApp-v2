import os
import jwt

from app import app
from functools import wraps
from flask import request, jsonify
from app.services.database import session, BlacklistedToken

def is_token_blacklisted(token):
    """Verifica si un token está en la lista negra."""
    blacklisted = session.query(BlacklistedToken).filter_by(token=token).first()
    return blacklisted is not None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token no proporcionado"}), 401

        try:
            token = token.split(" ")[1]  # Eliminar el prefijo "Bearer"
            if is_token_blacklisted(token):
                return jsonify({"message": "Token ha sido revocado"}), 401
            
            data = jwt.decode(token, app.secret_key, algorithms=["HS256"])

            if data.get("privilege") != "yes":
                return jsonify({"message": "Acceso denegado"}), 403
            
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token ha expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token invalido"}), 401

        return f(*args, **kwargs)
    return decorated

def require_allowed_origin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        allowed_origin = os.getenv("ALLOWED_ORIGIN")
        origin = request.headers.get('Origin') or request.headers.get('Referer')

        if not origin or not origin.startswith(allowed_origin):
            return jsonify({"error": "Access denied: Invalid origin"}), 403

        return f(*args, **kwargs)
    return decorated_function