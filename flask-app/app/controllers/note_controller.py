import jwt

from flask import render_template, request, jsonify
from app import app
from app.utils.auth_utils import is_token_blacklisted
from app.services.database import session, Note, User
from datetime import datetime, timezone


# JWT Helper function
def validate_token_and_get_user_id():
    token = request.headers.get("Authorization")
    if not token:
        return {"error": "Token no proporcionado."}, 401

    try:
        token = token.split(" ")[1]

        if is_token_blacklisted(token):
            return {"error": "Token inválido o revocado."}, 401

        payload = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        return payload["user_id"], None
    except jwt.ExpiredSignatureError:
        return {"error": "El token ha expirado."}, 401
    except jwt.InvalidTokenError:
        return {"error": "Token inválido."}, 401

# Add, remove and edit note
# Add and remove category from a note
# Add, remove and edit note
@app.route("/notes/add", methods=["POST"])
def add_note():
    user_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(user_id), error

    data = request.get_json()
    required_fields = ['title', 'content']
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Los campos {', '.join(missing_fields)} son obligatorios."}), 400
    
    new_note = Note(
        title=data['title'],
        content=data['content'],
        user_id=user_id,
        created_at=datetime.now(timezone.utc)
    )

    session.add(new_note)
    session.commit()

    return jsonify({"success": "La nota se ha añadido correctamente."}), 200

@app.route("/notes/remove/<int:id>", methods=["DELETE"])
def rem_note(id):
    user_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(user_id), error

    note = session.query(Note).get(id)

    if note is None:
        return jsonify({"error": "Nota no encontrada."}), 404

    if user_id != note.user_id:
        return jsonify({"error": "No tienes permiso para eliminar esta nota."}), 403

    session.delete(note)
    session.commit()

    return jsonify({"success": "La nota se ha eliminado correctamente."}), 200

@app.route("/notes/edit/<int:id>", methods=["POST"])
def edit_note(id):
    user_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(user_id), error

    data = request.get_json()
    note = session.query(Note).get(id)

    required_fields = ['title', 'content']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"El campo {field} es obligatorio."}), 400

    if note is None:
        return jsonify({"error": "Nota no encontrada."}), 404

    if user_id != note.user_id:
        return jsonify({"error": "No tienes permiso para editar esta nota."}), 403

    fields_to_update = {field: data.get(field) for field in required_fields if data.get(field)}

    session.query(Note).filter(Note.id == id).update(fields_to_update, synchronize_session=False)
    session.commit()

    return jsonify({"success": "La nota se ha actualizado correctamente."}), 200

# Archive and Unarchive notes
@app.route("/notes/archive/<int:id>", methods=["POST"])
def archive_note(id):
    user_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(user_id), error

    data = request.get_json()
    note = session.query(Note).get(id)

    if note is None:
        return jsonify({"error": "Nota no encontrada."}), 404

    if user_id != note.user_id:
        return jsonify({"error": "No tienes permiso para archivar esta nota."}), 403

    if note.status == "archived":
        return jsonify({"error": "La nota ya está archivada."}), 403

    note.status = "archived"
    session.commit()

    return jsonify({"success": "La nota se ha archivado correctamente."}), 200

@app.route("/notes/unarchive/<int:id>", methods=["POST"])
def unarchive_note(id):
    user_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(user_id), error

    data = request.get_json()
    note = session.query(Note).get(id)

    if note is None:
        return jsonify({"error": "Nota no encontrada."}), 404

    if user_id != note.user_id:
        return jsonify({"error": "No tienes permiso para desarchivar esta nota."}), 403

    if note.status == "active":
        return jsonify({"error": "La nota ya está activa."}), 403

    note.status = "active"
    session.commit()

    return jsonify({"success": "La nota se ha desarchivado correctamente."}), 200

# Get All notes active and get all notes archived
@app.route("/user/notes", methods=["GET"])
def get_all_notes():
    user_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(user_id), error

    notes = session.query(Note).filter(Note.user_id == user_id).all()

    if not notes:
        return jsonify({"error": "Aún no tienes notas, ¿Qué esperas para añadir una nota? ;)"}), 404

    return jsonify([{
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.strftime("%d/%m/%Y"),
    } for note in notes]), 200

@app.route("/notes/<int:id>", methods=["GET"])
def get_note_by_id(id):
    user_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(user_id), error

    note = session.query(Note).get(id)

    if note is None:
        return jsonify({"error": "Nota no encontrada."}), 404

    if user_id != note.user_id:
        return jsonify({"error": "No tienes permiso para ver esta nota."}), 403

    return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.strftime("%d/%m/%Y"),
    }), 200

@app.route("/notes/latest/<int:user_id>", methods=["GET"])
def get_latest_note(user_id):
    user_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(user_id), error

    try:
        note = session.query(Note).filter(Note.user_id == user_id).order_by(Note.created_at.desc()).limit(1).one_or_none()
    except Exception as e:
        return jsonify({"error": f"Error al obtener la última nota: {str(e)}"}), 500

    if note:
        return jsonify({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.strftime("%d/%m/%Y %H:%M:%S"),
        }), 200
    else:
        return jsonify({"error": "No se han encontrado notas para el usuario."}), 404