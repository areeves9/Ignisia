from flask_smorest import Blueprint

bp = Blueprint(
    "auth", "auth", url_prefix="/api/v1/auth", description="Authentication API"
)

from . import routes
