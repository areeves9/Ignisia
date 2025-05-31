from marshmallow import Schema, fields


class AuthRequestSchema(Schema):
    username = fields.Str(required=True, metadata={"description": "Username"})
    password = fields.Str(required=True, metadata={"description": "Plaintext password"})


class AuthResponseSchema(Schema):
    access_token = fields.Str(metadata={"description": "JWT access token"})
    username = fields.Str(required=False, metadata={"description": "Username"})
