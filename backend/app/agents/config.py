"""Configuration helpers for agent models."""

from __future__ import annotations

import logging
import os
from typing import Literal

import dspy

logger = logging.getLogger(__name__)

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    logger.error("GOOGLE_API_KEY not configured; DSPy cannot initialize")
    raise ValueError("GOOGLE_API_KEY environment variable is required")

LM_MAP: dict[str, str] = {
    "quick": "gemini/gemini-2.5-flash",
    "deep": "gemini/gemini-2.5-pro",
}

_current_mode: str | None = None


def configure_lm(mode: Literal["quick", "deep"] | str) -> str:
    """Configure DSPy to use the language model backing the requested mode."""
    global _current_mode

    normalized = mode.lower() if isinstance(mode, str) else "deep"
    if normalized not in LM_MAP:
        normalized = "deep"

    if _current_mode == normalized:
        return LM_MAP[normalized]

    model_name = LM_MAP[normalized]
    logger.info("Configuring DSPy LM for mode %s -> %s", normalized, model_name)
    lm = dspy.LM(model_name, api_key=API_KEY, model_type="chat")
    dspy.configure(lm=lm)
    _current_mode = normalized
    return model_name
