from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from .env before anything else

from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import db, jwt, migrate


def create_app():
    """
    Application factory for the Ignisia Flask app.

    Initializes the Flask app with configuration, sets up extensions
    (SQLAlchemy, JWT, CORS), and registers application blueprints.

    Returns:
        Flask: Configured Flask application instance.
    """
    from app.auth import models

    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"*": {"origins": "*"}})  # ← Only call once

    # Register blueprints
    from app.simulate import bp as simulate_bp

    from .auth import bp as auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(simulate_bp)

    return app
