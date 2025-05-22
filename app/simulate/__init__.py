from flask import Blueprint

bp = Blueprint("simulate", __name__, url_prefix="/simulate")

from . import routes  # ensures routes are registered
