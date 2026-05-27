from flask import Flask
from src.config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    """Application factory to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    from src.routes import bp
    app.register_blueprint(bp)

    return app
