from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")

# Import routes so they register with the blueprint
from .routes import routes
