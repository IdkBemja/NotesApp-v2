import jwt

from flask import render_template, request, jsonify
from app import app
from app.controllers.app_controller import is_token_blacklisted
from app.services.database import session, Note, Category, User
from datetime import datetime


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
    required_fields = ['title', 'description', 'status', 'category', 'tags']
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Los campos {', '.join(missing_fields)} son obligatorios."}), 400
    
    new_note = Note(
        title=data['title'],
        description=data['description'],
        status=data['status'],
        tags=','.join(data['tags']),
        user_id=user_id
    )

    session.add(new_note)
    session.flush()

    for category_name in data['category']:
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            session.add(category)
            session.flush()
        new_note.categories.append(category)

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

    required_fields = ['title', 'description', 'tags']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"El campo {field} es obligatorio."}), 400

    if note is None:
        return jsonify({"error": "Nota no encontrada."}), 404

    if user_id != note.user_id:
        return jsonify({"error": "No tienes permiso para editar esta nota."}), 403

    fields_to_update = {field: data.get(field) for field in required_fields if data.get(field)}

    if 'tags' in fields_to_update:
        fields_to_update['tags'] = ', '.join(fields_to_update['tags'])

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
@app.route("/user/<int:user_id>/active_notes", methods=["GET"])
def get_all_active_notes(user_id):
    requester_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(requester_id), error

    if requester_id != user_id:
        return jsonify({"error": "No tienes permiso para ver estas notas."}), 403

    notes = session.query(Note).filter(Note.user_id == user_id, Note.status == "active").all()

    if not notes:
        return jsonify({"error": "No se encontraron notas activas para este usuario."}), 404

    notes_list = [{"id": note.id, 
                   "title": note.title, 
                   "description": note.description, 
                   "status": note.status, 
                   "categories": [category.name for category in note.categories], 
                   "tags": note.tags, 
                   "updated_at": note.updated_at.strftime("%d/%m/%Y") 
                   if note.updated_at else note.created_at.strftime("%d/%m/%Y")} 
                   for note in notes]

    return jsonify(notes_list), 200

@app.route("/user/<int:user_id>/archived_notes", methods=["GET"])
def get_all_archived_notes(user_id):
    requester_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(requester_id), error

    if requester_id != user_id:
        return jsonify({"error": "No tienes permiso para ver estas notas."}), 403

    notes = session.query(Note).filter(Note.user_id == user_id, Note.status == "archived").all()

    if not notes:
        return jsonify({"error": "No se encontraron notas archivadas para este usuario."}), 404

    notes_list = [{"id": note.id, 
                   "title": note.title, 
                   "description": note.description, 
                   "status": note.status, 
                   "categories": [category.name for category in note.categories], 
                   "tags": note.tags, "updated_at": note.updated_at.strftime("%d/%m/%Y") 
                   if note.updated_at else note.created_at.strftime("%d/%m/%Y")} 
                   for note in notes]

    return jsonify(notes_list), 200

@app.route("/notes/latest/<int:user_id>", methods=["GET"])
def get_latest_note(user_id):
    user_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(user_id), error

    note = session.query(Note).filter(Note.user_id == user_id).order_by(Note.created_at.desc()).first()

    if note:
        return jsonify({
            "id": note.id,
            "title": note.title,
            "description": note.description,
            "tags": note.tags.split(', '),
            "categories": [category.name for category in note.categories],
            "created_at": note.created_at.strftime("%d/%m/%Y"),
            "updated_at": note.updated_at.strftime("%d/%m/%Y") if note.updated_at else None
        }), 200
    else:
        return jsonify({"error": "No se han encontrado notas para el usuario."}), 404


# add and remove category from a note

@app.route("/notes/<int:id>/categories", methods=["POST"])
def add_category_to_note(id):
    user_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(user_id), error
    
    data = request.get_json()
    note = session.query(Note).get(id)
    category = session.query(Category).get(data.get('category_id'))

    if note is None or category is None:
        return jsonify({"error": "Nota o categoría no encontrada."}), 404

    if user_id != note.user_id:
        return jsonify({"error": "No tienes permiso para modificar esto."}), 403

    note.categories.append(category)
    session.commit()

    return jsonify({"success": "Se ha añadido exitosamente la categoría a la nota."}), 200

@app.route("/notes/<int:id>/categories/<int:category_id>", methods=["POST"])
def remove_category_from_note(id, category_id):
    user_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(user_id), error
        
    data = request.get_json()
    note = session.query(Note).get(id)
    category = session.query(Category).get(category_id)

    if note is None or category is None:
        return jsonify({"error": "Nota o categoría no encontrada."}), 404

    if user_id != note.user_id:
        return jsonify({"error": "No tienes permiso para modificar esto."}), 403

    note.categories.remove(category)
    session.commit()

    return jsonify({"success": "Se ha eliminado exitosamente la categoría de la nota."}), 200

@app.route("/notes/categories/<int:category_id>", methods=["GET"])
def get_notes_by_category(category_id):
    user_id, error = validate_token_and_get_user_id()
    if error:
        return jsonify(user_id), error

    category = session.query(Category).get(category_id)

    if category is None:
        return jsonify({"error": "Categoría no encontrada."}), 404

    notes = session.query(Note).filter(Note.categories.contains(category), Note.user_id == user_id).all()

    if not notes:
        return jsonify({"error": "No se encontraron notas para esta categoría."}), 404

    return jsonify([{
        "id": note.id,
        "title": note.title,
        "description": note.description,
        "tags": note.tags.split(', '),
        "categories": [category.name for category in note.categories],
        "created_at": note.created_at.strftime("%d/%m/%Y"),
        "updated_at": note.updated_at.strftime("%d/%m/%Y") if note.updated_at else None
    } for note in notes]), 200