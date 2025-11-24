"""Unit tests for the outfit recommender backend."""

import pytest
from app.main import app


def test_health_endpoint():
    """Test the health check endpoint returns healthy status."""
    with app.test_client() as client:
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data == {"status": "healthy"}


def test_analyze_endpoint_no_image():
    """Test the analyze endpoint without an image returns error."""
    with app.test_client() as client:
        response = client.post('/api/analyze')
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "No image file provided" in data["error"]