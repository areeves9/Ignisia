from flask_smorest import Blueprint

bp = Blueprint(
    "simulate",
    "simulate",
    url_prefix="/api/v1/simulate",
    description="Simulation API",
)

from . import routes  # ensures routes are registered
