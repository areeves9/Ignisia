from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(db.Model):
    """
    Represents a registered user in the Ignisia application.

    Attributes:
        id (int): Primary key.
        username (str): Unique username for login.
        password_hash (str): Hashed password for authentication.

    Methods:
        set_password(password): Hashes and stores the given plaintext password.
        check_password(password): Validates a plaintext password against the stored hash.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
