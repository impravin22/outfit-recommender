"""State definition for the multi-agent outfit recommendation system."""

from typing import Any, Dict, List, Optional, TypedDict


class AgentLogEntry(TypedDict, total=False):
    """Structured log entry emitted by an agent."""

    agent: str
    message: str
    level: str
    timestamp: str
    details: str


class AgentState(TypedDict):
    """Typed dictionary representing the state passed between agents.

    Attributes:
        original_image: Raw image bytes uploaded by the user
        user_query: User's question or request about the outfit
        visual_analysis: Extracted features from the image (cut, color, fabric)
        trend_summary: Current fashion trends relevant to the request
        final_report: Synthesized styling advice from the analysis agent
        generated_image_url: URL of the generated outfit recommendation image
        generation_prompt: Prompt used for downstream image generation
        agent_logs: Chronological record of agent activity
        analysis_mode: quick or deep analysis selector
        image_generation_error: Optional explanation when image generation fails
    """

    original_image: bytes
    user_query: str
    visual_analysis: Dict[str, Any]
    trend_summary: str
    final_report: str
    generated_image_url: str
    generation_prompt: str
    agent_logs: List[AgentLogEntry]
    analysis_mode: str
    image_generation_error: Optional[str]
