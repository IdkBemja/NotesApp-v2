import os
import requests


from app import app
from urllib.parse import urlparse
from flask import jsonify, request, make_response
from app.services.database import session, Note, User
from app.utils.auth_utils import require_allowed_origin, token_required


@app.route("/api/protected", methods=["GET"])
@token_required
#@require_allowed_origin
def protected_route():
    return jsonify({"success": "Acceso permitido."}), 200

@app.route("/api/admin/dashboard", methods=["GET", "POST", "OPTIONS"])
@token_required
def admin_dashboard():
    token = request.headers.get("Authorization")
    headers = {}

    if token:
        headers["Authorization"] = token
    

    response = requests.request(
        method=request.method,
        url=os.getenv("ALLOWED_ORIGIN") + "/admin/dashboard",
        headers=headers,
        data=request.get_data(),
        allow_redirects=False
    )

    content = response.content
    # Solo reescribimos si es HTML
    if "text/html" in response.headers.get("Content-Type", ""):
        html = content.decode(response.encoding or "utf-8")
        # Cambiamos referencias de /assets/... a /api/admin/assets/...
        html = html.replace('href="/assets/', 'href="/api/admin/assets/')
        html = html.replace('src="/assets/', 'src="/api/admin/assets/')
        content = html.encode("utf-8")

    # Construye la respuesta Flask
    excluded = {"content-encoding","content-length","transfer-encoding","connection"}
    flask_resp = make_response(content, response.status_code)
    for n, v in response.headers.items():
        if n.lower() not in excluded:
            flask_resp.headers[n] = v
    return flask_resp



@app.route("/api/admin", methods=["GET"])
@token_required
def admin_route():
    route_admin = os.getenv("ALLOWED_ORIGIN")
    if not route_admin:
        return jsonify({"error": "ALLOWED_ORIGIN no está configurado."}), 500

    # Validar que ALLOWED_ORIGIN sea una URL válida
    parsed_url = urlparse(route_admin)
    if not parsed_url.scheme or not parsed_url.netloc:
        return jsonify({"error": "ALLOWED_ORIGIN no es una URL válida."}), 500

    # Obtener el token del encabezado Authorization
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token no proporcionado."}), 401

    # Devolver una respuesta JSON con la URL de redirección y el token
    return jsonify({
        "redirect_url": f"{route_admin}/admin/dashboard",
        "headers": {
            "Authorization": token
        }
    }), 200

@app.route('/api/notes', methods=['GET'])
@token_required
@require_allowed_origin
def get_notes():
    notes = session.query(Note).all()

    if not notes:
        return jsonify({"message": "Notas no encontradas."}), 404
    
    notes_list = [
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": note.updated_at.strftime('%Y-%m-%d %H:%M:%S') if note.updated_at else None,
            "user_id": note.user_id if note.user_id else None
        } 
        for note in notes
    ]
    return jsonify(notes_list), 200

@app.route("/api/users", methods=["GET"])
@token_required
@require_allowed_origin
def get_users():
    users = session.query(User).all()

    if not users:
        return jsonify({"message": "No users found."}), 404

    users_list = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else None
        } 
        for user in users
    ]
    return jsonify(users_list), 200