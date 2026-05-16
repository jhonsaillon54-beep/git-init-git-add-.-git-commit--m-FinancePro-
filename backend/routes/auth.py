from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    return jsonify({
        "message": "Usuário criado com sucesso"
    }), 201

    users.append({
        "name": name,
        "email": email,
        "password": password
    })

    return jsonify({
        "message": "Conta criada com sucesso"
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({
                "token": "financepro_token",
                "user": {
                    "name": user["name"],
                    "email": user["email"]
                }
            })

    return jsonify({
        "error": "Email ou senha inválidos"
    }), 401