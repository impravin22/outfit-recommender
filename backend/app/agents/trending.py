"""Trending agent for fetching current fashion trends."""

import logging
from typing import Any, Dict

import dspy

from app.utils.logs import append_agent_log

logger = logging.getLogger(__name__)


def fetch_trends(state: Dict[str, Any]) -> Dict[str, str]:
    """Fetch current fashion trends relevant to the user's query and outfit context.

    Uses DSPy to generate context-aware trends based on:
    - Gender/style presentation
    - Current occasion level
    - User's stated goals

    Args:
        state: Current agent state containing visual_analysis and user_query

    Returns:
        Dictionary with trend_summary key containing context-appropriate trends
    """
    logger.info("Fetching context-aware fashion trends")

    visual = state.get("visual_analysis", {})
    user_query = state.get("user_query", "")

    gender_style = visual.get("gender_style", "unisex")
    occasion = visual.get("occasion", "casual")

    logger.debug(
        f"Fetching trends for: {gender_style} style, {occasion} occasion, query: {user_query[:50]}..."
    )
    append_agent_log(
        state,
        agent="trends",
        message="Collecting trend context",
        details={
            "gender_style": gender_style,
            "occasion": occasion,
            "mode": state.get("analysis_mode", "deep"),
        },
    )

    try:
        # Use DSPy to generate contextual trends
        from app.agents.dspy_signatures import FetchRelevantTrends

        trend_generator = dspy.ChainOfThought(FetchRelevantTrends)

        result = trend_generator(
            gender_style=gender_style, occasion=occasion, user_query=user_query
        )

        trends = result.trend_summary

        logger.info("Context-aware trends generated successfully")
        logger.debug(f"Trends: {trends[:100]}...")
        append_agent_log(
            state,
            agent="trends",
            message="Produced trend summary",
            details=trends[:300],
        )

    except Exception as e:
        logger.error(f"Error fetching trends: {e}", exc_info=True)
        # Fallback to generic trends
        trends = (
            f"Current fashion trends for {gender_style} {occasion} wear focus on "
            "quality fabrics, versatile pieces, and sustainable choices. "
            "Neutral colors and classic silhouettes remain popular."
        )
        append_agent_log(
            state,
            agent="trends",
            message="Failed to fetch trends; using fallback",
            level="warning",
            details=str(e),
        )

    return {"trend_summary": trends, "agent_logs": state.get("agent_logs", [])}
