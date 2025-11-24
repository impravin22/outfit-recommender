"""Analysis agent for synthesizing outfit recommendations."""

import logging
import os
from typing import Any, Dict

import dspy
from dotenv import load_dotenv

from app.utils.logs import append_agent_log

load_dotenv()

logger = logging.getLogger(__name__)

# Configure Gemini API
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    raise ValueError("GOOGLE_API_KEY environment variable is required")

# Model configuration - Fine-tuned model interface
BASE_MODEL = "gemini-2.5-pro"
FINE_TUNED_MODEL = BASE_MODEL  # In production: "tunedModels/fashion-stylist-v1-abc123"
USE_FINE_TUNED_MODEL = False
MODEL_NAME = FINE_TUNED_MODEL if USE_FINE_TUNED_MODEL else BASE_MODEL


def synthesize_advice(state: Dict[str, Any]) -> Dict[str, str]:
    """Synthesize styling advice from visual analysis and trends using DSPy.

    Uses DSPy Chain-of-Thought reasoning to generate context-aware advice that:
    - Matches gender/style presentation
    - Addresses user's specific request
    - References appropriate trends
    - Maintains or appropriately elevates formality

    Args:
        state: Agent state containing:
            - visual_analysis: Extracted features including gender_style
            - trend_summary: Context-appropriate fashion trends
            - user_query: User's specific question or request

    Returns:
        Dictionary with final_report key containing styling advice

    Raises:
        ValueError: If API key is not configured
    """
    logger.info("Synthesizing styling advice with DSPy")
    append_agent_log(
        state,
        agent="advisor",
        message="Generating styling advice",
        details={"mode": state.get("analysis_mode", "deep")},
    )

    visual = state.get("visual_analysis", {})
    trends = state.get("trend_summary", "")
    query = state.get("user_query", "")

    logger.debug(f"Processing query: {query}")
    logger.debug(f"Visual keys: {list(visual.keys())}")

    try:
        # Use DSPy for structured, context-aware advice generation
        from app.agents.dspy_signatures import SynthesizeStylingAdvice

        advisor = dspy.ChainOfThought(SynthesizeStylingAdvice)

        result = advisor(
            user_query=query,
            gender_style=visual.get("gender_style", "unisex"),
            cut=visual.get("cut", "unknown"),
            color=visual.get("color", "unknown"),
            fabric=visual.get("fabric", "unknown"),
            occasion=visual.get("occasion", "casual"),
            trends=trends,
        )

        advice = result.advice

        logger.info("Styling advice generated successfully")
        logger.debug(f"Advice length: {len(advice)} characters")
        append_agent_log(
            state,
            agent="advisor",
            message="Completed styling advice",
            details=advice[:300],
        )

    except Exception as e:
        logger.error(f"Error generating styling advice: {e}", exc_info=True)
        advice = (
            "Unable to generate personalized advice at this time. "
            "Please try again later or consult with a fashion professional."
        )
        append_agent_log(
            state,
            agent="advisor",
            message="Failed to generate styling advice",
            level="error",
            details=str(e),
        )

    return {"final_report": advice, "agent_logs": state.get("agent_logs", [])}
