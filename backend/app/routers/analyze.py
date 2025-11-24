"""Analyze endpoint for processing outfit recommendation requests."""

import logging
from typing import Any, Dict

from flask import Blueprint, jsonify, request
from werkzeug.datastructures import FileStorage

from app.agents.config import configure_lm
from app.agents.supervisor import agent_graph

logger = logging.getLogger(__name__)

analyze_bp = Blueprint("analyze", __name__)

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
DEFAULT_QUERY = "What should I wear for a wedding?"


def _allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension.

    Args:
        filename: Name of the uploaded file

    Returns:
        True if extension is allowed, False otherwise
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _validate_request() -> tuple[FileStorage, str] | tuple[Dict[str, str], int]:
    """Validate the incoming request for required fields and constraints.

    Returns:
        Tuple of (file, user_query) if valid, or (error_response, status_code)
    """
    if "image" not in request.files:
        logger.warning("Request missing image file")
        return {"error": "No image file provided"}, 400

    file = request.files["image"]

    if file.filename == "":
        logger.warning("Empty filename provided")
        return {"error": "No file selected"}, 400

    if not _allowed_file(file.filename):
        logger.warning(f"Invalid file extension: {file.filename}")
        return {
            "error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        }, 400

    user_query = request.form.get("query", DEFAULT_QUERY)

    return file, user_query


@analyze_bp.route("/analyze", methods=["POST"])
def analyze_outfit() -> tuple[Any, int]:
    """Analyze uploaded outfit image and provide styling recommendations.

    This endpoint orchestrates the multi-agent workflow:
    1. Validates the uploaded image
    2. Analyzes visual features using Gemini Vision
    3. Fetches current fashion trends
    4. Synthesizes personalized styling advice
    5. Generates outfit recommendation image

    Request:
        - Form data with 'image' file and optional 'query' text

    Returns:
        JSON response containing:
        - visual_analysis: Extracted features (cut, color, fabric, occasion)
        - trend_summary: Current fashion trends
        - final_report: Personalized styling advice
        - generated_image_url: URL of generated outfit image

    Status Codes:
        200: Success
        400: Invalid request (missing file, wrong format)
        500: Server error during processing
    """
    logger.info("Received analyze request")

    # Validate request
    validation_result = _validate_request()
    if isinstance(validation_result[0], dict):  # Error response
        return jsonify(validation_result[0]), validation_result[1]

    file, user_query = validation_result
    logger.info(f"Processing image: {file.filename}, query: {user_query[:50]}...")

    try:
        # Read image bytes
        image_bytes = file.read()

        if len(image_bytes) > MAX_FILE_SIZE:
            logger.warning(f"File too large: {len(image_bytes)} bytes")
            return jsonify({"error": "File size exceeds 10MB limit"}), 400

        logger.debug(f"Image size: {len(image_bytes)} bytes")

        analysis_mode = request.form.get("mode", "deep").lower()
        if analysis_mode not in {"quick", "deep"}:
            analysis_mode = "deep"

        configure_lm(analysis_mode)
        logger.info("Configured analysis mode: %s", analysis_mode)

        # Initialize agent state
        initial_state = {
            "original_image": image_bytes,
            "user_query": user_query,
            "visual_analysis": {},
            "trend_summary": "",
            "final_report": "",
            "generated_image_url": "",
            "generation_prompt": "",
            "agent_logs": [],
            "analysis_mode": analysis_mode,
            "image_generation_error": None,
        }

        # Invoke LangGraph multi-agent workflow
        logger.info("Invoking agent graph")
        result = agent_graph.invoke(initial_state)

        # Prepare response (exclude raw bytes)
        response_data = {
            "visual_analysis": result.get("visual_analysis"),
            "trend_summary": result.get("trend_summary"),
            "final_report": result.get("final_report"),
            "generated_image_url": result.get("generated_image_url"),
            "agent_logs": result.get("agent_logs", []),
            "analysis_mode": analysis_mode,
            "generation_prompt": result.get("generation_prompt"),
            "image_generation_error": result.get("image_generation_error"),
        }

        logger.info("Request processed successfully")
        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
