"""Multi-model agent for image analysis and generation using Google Gemini."""

import base64
import io
import logging
import os
from typing import Any, Dict, Optional
from urllib import request as urllib_request

import dspy
import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai import files as genai_files
from google.generativeai import types as genai_types
from PIL import Image

from app.utils.logs import append_agent_log

load_dotenv()

logger = logging.getLogger(__name__)

# Configure Gemini API
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    raise ValueError("GOOGLE_API_KEY environment variable is required")

genai.configure(api_key=API_KEY)

# Model configuration
VISION_MODELS = {
    "quick": "gemini-2.5-flash",
    "deep": "gemini-2.5-pro",
}

IMAGE_MODEL = "gemini-2.5-flash-image"  # For direct Gemini image generation


def analyze_image(state: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Analyze outfit image using Gemini Vision to extract visual features.

    Uses Google's Gemini multimodal model with DSPy for structured output
    to analyze the uploaded image and extract information including gender
    presentation, cut, color, fabric, and suitable occasions.

    Args:
        state: Agent state containing original_image bytes and user_query

    Returns:
        Dictionary with visual_analysis key containing extracted features

    Raises:
        ValueError: If image cannot be processed
    """
    mode = state.get("analysis_mode", "deep")
    vision_model = VISION_MODELS.get(mode, VISION_MODELS["deep"])

    logger.info("Starting image analysis with %s + DSPy", vision_model)
    append_agent_log(
        state,
        agent="vision",
        message="Starting image analysis",
        details={"mode": mode, "model": vision_model},
    )

    try:
        model = genai.GenerativeModel(vision_model)

        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(state["original_image"]))
        logger.debug(f"Image loaded: {image.size} pixels")

        # First, get a detailed description of the image
        desc_prompt = """
        Describe this outfit image in detail. Include:
        - Gender presentation (masculine/feminine/unisex)
        - Type of garments (shirt, pants, dress, etc.)
        - Style and fit
        - Colors and patterns
        - Apparent fabric types
        - Overall vibe and formality level
        """

        desc_response = model.generate_content([desc_prompt, image])
        image_description = desc_response.text

        logger.debug(f"Image description: {image_description[:200]}...")

        # Use DSPy to structure the analysis
        from app.agents.dspy_signatures import AnalyzeOutfitImage

        analyzer = dspy.ChainOfThought(AnalyzeOutfitImage)

        result = analyzer(
            image_description=image_description, user_query=state.get("user_query", "")
        )

        analysis = {
            "gender_style": result.gender_style,
            "cut": result.cut,
            "color": result.color,
            "fabric": result.fabric,
            "occasion": result.occasion,
        }

        logger.info("Image analysis completed successfully")
        logger.debug(f"Analysis result: {analysis}")

        append_agent_log(
            state,
            agent="vision",
            message="Completed image analysis",
            details=analysis,
        )

    except Exception as e:
        logger.error(f"Error in analyze_image: {e}", exc_info=True)
        analysis = {
            "gender_style": "unknown",
            "cut": "unknown",
            "color": "unknown",
            "fabric": "unknown",
            "occasion": "unknown",
            "error": str(e),
        }
        append_agent_log(
            state,
            agent="vision",
            message="Failed to analyze image",
            level="error",
            details=str(e),
        )

    return {"visual_analysis": analysis, "agent_logs": state.get("agent_logs", [])}


def generate_outfit(state: Dict[str, Any]) -> Dict[str, str]:
    """Generate outfit visualization prompt and metadata.

    Note: Imagen 3 is a separate Google Cloud AI service not available through
    the Gemini API. This function prepares the generation prompt and returns
    metadata. In production, integrate with:
    - Google Cloud Vertex AI Imagen API
    - Alternative: Stable Diffusion, DALL-E 3, or Midjourney API
    - Alternative: Use Gemini to generate detailed shopping links

    Args:
        state: Agent state containing final_report and visual_analysis

    Returns:
        Dictionary with generated_image_url and generation_prompt
    """
    logger.info("Preparing outfit visualization")
    state["image_generation_error"] = None
    append_agent_log(
        state,
        agent="generator",
        message="Preparing outfit visualization",
        details={
            "mode": state.get("analysis_mode", "deep"),
            "has_advice": bool(state.get("final_report")),
        },
    )

    try:
        # Extract styling advice and visual features
        advice = state.get("final_report", "")
        visual = state.get("visual_analysis", {})
        query = state.get("user_query", "")

        # Create detailed prompt for image generation (ready for Imagen/other APIs)
        generation_prompt = f"""
Professional fashion editorial photography:
- Outfit: {advice.split(".")[0] if advice else "Professional outfit"}
- Style: {visual.get("cut", "modern tailored fit")}
- Colors: {visual.get("color", "neutral professional tones")}
- Fabric: {visual.get("fabric", "high-quality materials")}
- Occasion: {visual.get("occasion", "professional setting")}
- Personal request: {query or "Tailor to the user's stated preference"}
- IMPORTANT: Keep the exact same person, face, facial expression, pose, and background from the reference image. Only change the clothing/outfit to match the new style guidance.
- Setting: Same background as reference image, professional lighting
- Shot: Full body, same pose and composition as reference image, high detail, 8K quality
- Mood: Sophisticated, professional, current trends
- Reference: Use the provided outfit photo as base - preserve the person's identity, face, hair, body type, pose, and background completely unchanged. Only modify the wardrobe items.
        """.strip()

        logger.debug(
            f"Generated prompt for image generation: {generation_prompt[:100]}..."
        )

        reference_image_bytes = state.get("original_image")

        generated_url, mime_type = _generate_image_from_gemini(
            generation_prompt,
            base_image=reference_image_bytes,
            stylist_advice=advice,
        )

        if generated_url:
            logger.info(
                "Outfit visualization generated successfully with Gemini 2.5 Flash Image"
            )
            append_agent_log(
                state,
                agent="generator",
                message="Generated upgraded outfit image",
                details={"mime_type": mime_type or "unknown"},
            )
        else:
            logger.warning(
                "Gemini image generation returned empty payload; skipping image output"
            )
            generated_url = None
            state["image_generation_error"] = (
                "Gemini image generation returned no content"
            )
            append_agent_log(
                state,
                agent="generator",
                message="Gemini image generation returned no content",
                level="warning",
            )

    except Exception as e:
        logger.error(f"Error preparing outfit visualization: {e}", exc_info=True)
        generated_url = None
        state["image_generation_error"] = str(e)
        append_agent_log(
            state,
            agent="generator",
            message="Failed to generate outfit visualization",
            level="error",
            details=str(e),
        )

    return {
        "generated_image_url": generated_url,
        "generation_prompt": generation_prompt
        if "generation_prompt" in locals()
        else "",
        "image_generation_error": state.get("image_generation_error"),
        "agent_logs": state.get("agent_logs", []),
    }


def _generate_image_from_gemini(
    prompt: str,
    base_image: Optional[bytes] = None,
    stylist_advice: Optional[str] = None,
) -> tuple[Optional[str], Optional[str]]:
    """Generate an outfit image using Gemini 2.5 Flash Image.

    Args:
        prompt: Natural language description of the desired outfit visualization.
        base_image: Optional reference outfit image provided by the user.
        stylist_advice: Optional narrative guidance from the stylist agent.

    Returns:
        Tuple containing a data URL for the generated image (or None) and the mime type.
    """

    try:
        image_model = genai.GenerativeModel(IMAGE_MODEL)

        messages: list[Any] = [
            "Generate a new image that keeps the exact same person, face, facial expression, pose, body type, and background from the reference image. Only change the clothing and outfit to match the professional styling guidance provided. Do not alter the person's appearance, hair, or any other physical features.",
        ]

        if stylist_advice:
            messages.append(f"Styling guidance to apply:\n{stylist_advice}")

        messages.append(prompt)

        if base_image:
            try:
                reference_image = Image.open(io.BytesIO(base_image))
                reference_image.load()
                messages.append(reference_image)
            except Exception:
                logger.warning(
                    "Unable to load reference image for Gemini generation",
                    exc_info=True,
                )

        response = image_model.generate_content(
            messages,
            generation_config=genai_types.GenerationConfig(
                temperature=0.7,
                candidate_count=1,
            ),
        )

        image_bytes, mime_type = _extract_image_bytes(response)
        if not image_bytes:
            return None, None

        encoded = base64.b64encode(image_bytes).decode("utf-8")
        mime_type = mime_type or "image/png"
        return f"data:{mime_type};base64,{encoded}", mime_type

    except Exception:
        logger.exception("Gemini image generation failed")
        return None, None


def _extract_image_bytes(response) -> tuple[Optional[bytes], Optional[str]]:
    """Extract raw image bytes from a Gemini generate_content response."""

    if not response:
        return None, None

    # Response may expose parts directly or through candidates.
    parts_iterables = []

    if hasattr(response, "candidates"):
        for candidate in response.candidates or []:
            content = getattr(candidate, "content", None)
            if content and hasattr(content, "parts"):
                parts_iterables.append(content.parts)

    if hasattr(response, "parts") and response.parts:
        parts_iterables.append(response.parts)

    for parts in parts_iterables:
        for part in parts or []:
            inline_data = getattr(part, "inline_data", None)
            if inline_data and getattr(inline_data, "data", None):
                mime_type = getattr(inline_data, "mime_type", None)
                data = inline_data.data
                if isinstance(data, bytes):
                    return data, mime_type
                if isinstance(data, str):
                    try:
                        return base64.b64decode(data), mime_type
                    except Exception:
                        logger.debug(
                            "Unable to decode inline data string from Gemini response",
                            exc_info=True,
                        )

            file_data = getattr(part, "file_data", None)
            if file_data and getattr(file_data, "file_uri", None):
                file_uri = file_data.file_uri
                mime_type = getattr(file_data, "mime_type", None)
                data = _download_file_bytes(file_uri)
                if data:
                    return data, mime_type

    return None, None


def _download_file_bytes(file_uri: str) -> Optional[bytes]:
    """Download file bytes using the Files API reference."""

    try:
        file_ref = genai_files.get_file(file_uri)
        uri = getattr(file_ref, "uri", None)
        if not uri:
            return None

        with urllib_request.urlopen(uri) as response:
            return response.read()
    except Exception:
        logger.debug("Failed to fetch Gemini file asset", exc_info=True)
        return None
