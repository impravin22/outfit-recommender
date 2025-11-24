"""Main Flask application entry point for outfit recommender backend."""

import logging

from flask import Flask
from flask_cors import CORS

from app.routers.analyze import analyze_bp
from app.routers.healthcheck import health_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    CORS(app)  # Enable CORS for frontend communication

    # Register Blueprints
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(analyze_bp, url_prefix="/api")

    logger.info("Flask application initialized successfully")
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
