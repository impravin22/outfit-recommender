"""Health check endpoint for monitoring service availability."""

from typing import Any, Dict

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check() -> tuple[Dict[str, Any], int]:
    """Check if the service is running and healthy.

    Returns:
        JSON response with status and HTTP 200 code
    """
    return jsonify({"status": "ok"}), 200
