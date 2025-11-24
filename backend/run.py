#!/usr/bin/env python3
"""Simple runner script for the Flask backend."""

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.main import app  # noqa: E402

if __name__ == "__main__":
    print("Starting Flask backend on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
