from flask import request, jsonify

from app import app
from app.services.database import BlacklistedToken, User, session
from flask_bcrypt import Bcrypt

import jwt
from datetime import datetime, timedelta

bcrypt = Bcrypt(app)

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "username": session.query(User).filter_by(id=user_id).first().username,
        "exp": datetime.utcnow() + timedelta(hours=1)  # Expira en 1 hora
    }
    token = jwt.encode(payload, app.secret_key, algorithm="HS256")
    return token

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = session.query(User).filter_by(username=username).first()

    if user is None:
        return jsonify({"message": "Cuenta no encontrada."}), 404

    if user and bcrypt.check_password_hash(user.password, password):
        token = generate_token(user.id)
        return jsonify({"success": "Inicio sesión válido.", "token": token}), 200
    else:
        return jsonify({"message": "Credenciales inválidas."}), 401


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    required_fields = ['username', 'email', 'password', 'confirm_password']

    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"El campo {field} es obligatorio."}), 400

    username = data['username']
    email = data['email']
    password = data['password']
    password2 = data['confirm_password']

    if username == password:
        return jsonify({"message": "El nombre de usuario y la contraseña no pueden ser iguales."}), 400

    if len(username) < 4:
        return jsonify({"message": "El nombre de usuario debe tener más de 4 caracteres."}), 400

    if len(password) < 5:
        return jsonify({"message": "La contraseña debe tener más de 5 caracteres."}), 400

    if password != password2:
        return jsonify({"message": "Las contraseñas no coinciden."}), 400

    user = session.query(User).filter(User.username == username).first()
    if user:
        return jsonify({"message": "El nombre de usuario ya existe en el sistema."}), 409
    
    email_exists = session.query(User).filter(User.email == email).first()
    if email_exists:
        return jsonify({"message": "El correo electrónico ya existe en el sistema."}), 409

    pass_bcrypt = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username=username, password=pass_bcrypt, email=email)

    session.add(new_user)
    session.commit()
    token = generate_token(new_user.id)

    return jsonify({"success": "El usuario ha sido registrado exitosamente.",
                    "token": token}), 201


@app.route("/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token no proporcionado."}), 401

    try:
        token = token.split(" ")[1]

        blacklisted_token = BlacklistedToken(token=token)
        session.add(blacklisted_token)
        session.commit()

        return jsonify({"message": "Sesión cerrada exitosamente."}), 200
    except Exception as e:
        return jsonify({"message": "Error al cerrar sesión.", "error": str(e)}), 500

@app.route("/api/get_user/<int:userid>", methods=["GET"])
def get_user(userid):
    user = session.query(User).filter_by(id=userid).first()

    if user is None:
        return jsonify({"message": "Usuario no encontrado."}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }), 200
