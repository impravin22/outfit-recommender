"""Utilities for recording agent activity logs in the shared state."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict


def append_agent_log(
    state: Dict[str, Any],
    agent: str,
    message: str,
    *,
    level: str = "info",
    details: Any | None = None,
) -> None:
    """Append a structured log entry to the agent state.

    Args:
        state: Current agent state dictionary (mutated in place).
        agent: Short name of the agent writing the log.
        message: Human readable message summarizing the event.
        level: Optional severity level (info, warning, error).
        details: Optional payload for additional context; converted to string.
    """

    logs = state.setdefault("agent_logs", [])

    timestamp = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )

    entry: Dict[str, Any] = {
        "agent": agent,
        "message": message,
        "level": level,
        "timestamp": timestamp,
    }

    if details is not None:
        if isinstance(details, (dict, list)):
            entry["details"] = json.dumps(details, ensure_ascii=True)[:800]
        else:
            entry["details"] = str(details)

    logs.append(entry)
    state["agent_logs"] = logs
