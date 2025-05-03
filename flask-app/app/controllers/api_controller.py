from app import app
from flask import jsonify, request
from app.services.database import session, Note, User
from app.utils.auth_utils import token_required


@app.route("/api/protected", methods=["GET"])
@token_required
def protected_route():
    return jsonify({"success": "Accesso permitido."}), 200

@app.route('/api/notes', methods=['GET'])
@token_required
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