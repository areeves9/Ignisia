from marshmallow import fields

from app.extensions import ma


class AuthRequestSchema(ma.Schema):
    username = fields.Str(required=True, metadata={"description": "Username"})
    password = fields.Str(required=True, metadata={"description": "Plaintext password"})


class AuthResponseSchema(ma.Schema):
    access_token = fields.Str(metadata={"description": "JWT access token"})


class MessageResponseSchema(ma.Schema):
    msg = fields.Str(metadata={"description": "Response message"})
