"""Supervisor module for orchestrating the multi-agent workflow using LangGraph."""

import logging
from typing import Any

from langgraph.graph import END, StateGraph

from .analysis import synthesize_advice
from .multi_model import analyze_image, generate_outfit
from .state import AgentState
from .trending import fetch_trends

logger = logging.getLogger(__name__)


def build_graph() -> Any:
    """Construct the LangGraph workflow for outfit recommendation.

    This creates a sequential pipeline that:
    1. Analyzes the uploaded image to extract visual features
    2. Fetches current fashion trends
    3. Synthesizes styling advice combining visual analysis and trends
    4. Generates a new outfit image based on the recommendations

    Returns:
        Compiled LangGraph ready for execution
    """
    builder = StateGraph(AgentState)

    # Add nodes
    builder.add_node("analyze_image", analyze_image)
    builder.add_node("fetch_trends", fetch_trends)
    builder.add_node("synthesize_advice", synthesize_advice)
    builder.add_node("generate_outfit", generate_outfit)

    # Define edges - sequential flow
    builder.set_entry_point("analyze_image")
    builder.add_edge("analyze_image", "fetch_trends")
    builder.add_edge("fetch_trends", "synthesize_advice")
    builder.add_edge("synthesize_advice", "generate_outfit")
    builder.add_edge("generate_outfit", END)

    logger.info("Agent graph built successfully")
    return builder.compile()


# Singleton instance of the graph
agent_graph = build_graph()
