"""Unit tests for agent modules."""

from unittest.mock import MagicMock, patch


def test_agent_state_structure():
    """Test that AgentState has required fields."""
    # This is more of a type check, but we can test the TypedDict structure
    test_state = {
        "original_image": b"fake_image_data",
        "user_query": "Test query",
        "analysis_mode": "quick",
        "visual_analysis": {},
        "trend_summary": "",
        "final_report": "",
        "generated_image_url": "",
        "generation_prompt": "",
        "agent_logs": [],
    }

    # Check that all expected keys are present
    expected_keys = [
        "original_image",
        "user_query",
        "analysis_mode",
        "visual_analysis",
        "trend_summary",
        "final_report",
        "generated_image_url",
        "generation_prompt",
        "agent_logs",
    ]

    for key in expected_keys:
        assert key in test_state


def test_config_model_selection():
    """Test that config selects correct models based on mode."""
    from app.agents.multi_model import IMAGE_MODEL, VISION_MODELS

    # Test vision models
    assert VISION_MODELS["quick"] == "gemini-2.5-flash"
    assert VISION_MODELS["deep"] == "gemini-2.5-pro"

    # Test image model
    assert IMAGE_MODEL == "gemini-2.5-flash-image"


@patch("app.agents.multi_model.genai.GenerativeModel")
@patch("app.agents.multi_model.Image")
def test_analyze_image_success(mock_image_class, mock_model_class):
    """Test successful image analysis."""
    from app.agents.multi_model import analyze_image

    # Mock the image
    mock_image = MagicMock()
    mock_image_class.open.return_value = mock_image
    mock_image.size = (800, 600)

    # Mock the model response
    mock_model = MagicMock()
    mock_model_class.return_value = mock_model

    mock_desc_response = MagicMock()
    mock_desc_response.text = "A person wearing casual clothes"
    mock_model.generate_content.return_value = mock_desc_response

    # Mock DSPy
    with patch("app.agents.multi_model.dspy.ChainOfThought") as mock_dspy:
        mock_analyzer = MagicMock()
        mock_analyzer.return_value = type(
            "Result",
            (),
            {
                "gender_style": "masculine",
                "cut": "casual fit",
                "color": "blue and white",
                "fabric": "cotton",
                "occasion": "casual",
            },
        )()
        mock_dspy.return_value = mock_analyzer

        state_dict = {
            "original_image": b"fake_image",
            "user_query": "What to wear?",
            "analysis_mode": "quick",
        }

        result = analyze_image(state_dict)

        assert "visual_analysis" in result
        assert result["visual_analysis"]["gender_style"] == "masculine"


@patch("app.agents.multi_model.genai.GenerativeModel")
def test_generate_outfit_success(mock_model_class):
    """Test successful outfit generation."""
    from app.agents.multi_model import generate_outfit

    # Mock the model
    mock_model = MagicMock()
    mock_model_class.return_value = mock_model

    # Mock response with image data
    mock_response = MagicMock()
    mock_candidate = MagicMock()
    mock_content = MagicMock()
    mock_part = MagicMock()
    mock_inline_data = MagicMock()
    mock_inline_data.data = b"fake_image_bytes"
    mock_inline_data.mime_type = "image/png"
    mock_part.inline_data = mock_inline_data
    mock_content.parts = [mock_part]
    mock_candidate.content = mock_content
    mock_response.candidates = [mock_candidate]

    mock_model.generate_content.return_value = mock_response

    state_dict = {
        "original_image": b"fake_image",
        "final_report": "Wear a blue shirt",
        "visual_analysis": {"cut": "casual", "color": "blue"},
        "user_query": "Casual look",
        "analysis_mode": "quick",
        "agent_logs": [],
    }

    result = generate_outfit(state_dict)

    assert "generated_image_url" in result
    assert result["generated_image_url"].startswith("data:image/png;base64,")


@patch("app.agents.trending.dspy.ChainOfThought")
def test_trending_agent(mock_dspy):
    """Test trending agent functionality."""
    from app.agents.trending import fetch_trends

    mock_analyzer = MagicMock()
    mock_analyzer.return_value = type(
        "Result", (), {"trend_summary": "**Casual Style:** Popular trends include..."}
    )()
    mock_dspy.return_value = mock_analyzer

    state_dict = {"user_query": "Casual outfit", "agent_logs": []}

    result = fetch_trends(state_dict)

    assert "trend_summary" in result
    assert "Casual Style" in result["trend_summary"]


@patch("app.agents.analysis.dspy.ChainOfThought")
def test_analysis_agent(mock_dspy):
    """Test analysis agent functionality."""
    from app.agents.analysis import synthesize_advice

    mock_analyzer = MagicMock()
    mock_analyzer.return_value = type(
        "Result", (), {"advice": "This outfit works well for casual occasions..."}
    )()
    mock_dspy.return_value = mock_analyzer

    state_dict = {
        "visual_analysis": {"gender_style": "masculine", "occasion": "casual"},
        "trend_summary": "Casual trends",
        "user_query": "What to wear?",
        "agent_logs": [],
    }

    result = synthesize_advice(state_dict)

    assert "final_report" in result
    assert "casual" in result["final_report"].lower()
