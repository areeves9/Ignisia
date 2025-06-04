from flask import jsonify, make_response
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_csrf_token,
    get_jwt_identity,
    jwt_required,
    set_refresh_cookies,
)

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
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            csrf_token = get_csrf_token(refresh_token)

            response = make_response(
                jsonify(
                    {
                        "access_token": access_token,
                        "username": user.username,
                        "csrf_token": csrf_token,
                    }
                )
            )

            response.set_cookie(
                "csrf_refresh_token",
                csrf_token,
                httponly=False,  # must be readable by JS
                secure=True,
                samesite="Strict",
                path="/",
            )

            set_refresh_cookies(response, refresh_token)

            return response
        return {"msg": "Bad credentials"}, 401


class LogoutResource(MethodView):
    def post(self):
        response = make_response(jsonify({"msg": "Logout successful"}))
        response.set_cookie(
            "refresh_token",
            "",
            max_age=0,
            path="/refresh",
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        return response


class RefreshResource(MethodView):
    @jwt_required(refresh=True)
    @bp.response(200, AuthResponseSchema)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {"access_token": access_token}, 200


bp.add_url_rule("/register", view_func=RegisterResource.as_view("register"))
bp.add_url_rule("/login", view_func=LoginResource.as_view("login"))
bp.add_url_rule("/refresh", view_func=RefreshResource.as_view("refresh"))
bp.add_url_rule("/logout", view_func=LogoutResource.as_view("logout"))
