from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

from app.auth.models import User
from app.extensions import db

from . import bp
from .serializers import AuthRequestSchema, AuthResponseSchema


class RegisterResource(MethodView):
    @bp.arguments(AuthRequestSchema)
    @bp.response(201, AuthResponseSchema)
    def post(self, data):
        if User.query.filter_by(username=data["username"]).first():
            return {"msg": "User already exists"}, 409

        user = User(username=data["username"])
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))
        return {"access_token": token, "username": user.username}, 201


class LoginResource(MethodView):
    @bp.arguments(AuthRequestSchema)
    @bp.response(200, AuthResponseSchema)
    def post(self, data):
        user = User.query.filter_by(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            token = create_access_token(identity=str(user.id))
            return {"access_token": token}
        return {"msg": "Bad credentials"}, 401


bp.add_url_rule("/register", view_func=RegisterResource.as_view("register"))
bp.add_url_rule("/login", view_func=LoginResource.as_view("login"))
