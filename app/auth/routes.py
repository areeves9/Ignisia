from flask import jsonify, request
from flask_jwt_extended import create_access_token

from app.auth.models import User
from app.extensions import db

from . import bp  # the Blueprint from __init__.py


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 409

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=str(user.id))
        return jsonify(access_token=token)

    return jsonify({"msg": "Bad credentials"}), 401
