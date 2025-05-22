from flask import jsonify, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

from app.auth.models import User
from app.extensions import db

from . import bp
from .serializers import AuthRequestSchema, AuthResponseSchema, MessageResponseSchema

auth_request_schema = AuthRequestSchema()
token_response_schema = AuthResponseSchema()
msg_response_schema = MessageResponseSchema()


@bp.route("/register", methods=["POST"])
def register():
    try:
        data = auth_request_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    username = data["username"]
    password = data["password"]

    if User.query.filter_by(username=username).first():
        return msg_response_schema.dump({"msg": "User already exists"}), 409

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return msg_response_schema.dump({"msg": "User created"}), 201


@bp.route("/login", methods=["POST"])
def login():
    try:
        data = auth_request_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=str(user.id))
        return token_response_schema.dump({"access_token": token}), 200

    return msg_response_schema.dump({"msg": "Bad credentials"}), 401
