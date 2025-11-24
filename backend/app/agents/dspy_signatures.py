"""DSPy signatures for the outfit recommendation system."""

import dspy


class AnalyzeOutfitImage(dspy.Signature):
    """Analyze an outfit image to extract visual features.

    Focus on identifying:
    - Gender/style presentation of the outfit
    - Cut and silhouette details
    - Color palette
    - Fabric types
    - Suitable occasions
    """

    image_description: str = dspy.InputField(
        desc="Detailed description of the outfit image"
    )
    user_query: str = dspy.InputField(desc="User's specific question or request")

    gender_style: str = dspy.OutputField(
        desc="Gender presentation: masculine, feminine, unisex, or non-binary"
    )
    cut: str = dspy.OutputField(desc="Detailed description of cut and silhouette")
    color: str = dspy.OutputField(desc="Dominant and accent colors")
    fabric: str = dspy.OutputField(desc="Fabric type and texture")
    occasion: str = dspy.OutputField(desc="Suitable occasions for this outfit")


class FetchRelevantTrends(dspy.Signature):
    """Fetch fashion trends relevant to the specific outfit context.

    Trends should match:
    - Gender/style presentation
    - Formality level
    - Occasion type
    - User's stated goals
    """

    gender_style: str = dspy.InputField(desc="Gender presentation of outfit")
    occasion: str = dspy.InputField(desc="Current outfit occasion level")
    user_query: str = dspy.InputField(desc="User's styling goals")

    trend_summary: str = dspy.OutputField(
        desc="Relevant fashion trends matching the outfit context and user goals"
    )


class SynthesizeStylingAdvice(dspy.Signature):
    """Generate personalized styling advice based on visual analysis and trends.

    Advice must:
    - Match the gender/style presentation
    - Address user's specific request
    - Be practical and actionable
    - Reference appropriate trends
    - Maintain outfit formality level or elevate appropriately
    """

    user_query: str = dspy.InputField(desc="User's specific request")
    gender_style: str = dspy.InputField(desc="Gender presentation")
    cut: str = dspy.InputField(desc="Current outfit cut")
    color: str = dspy.InputField(desc="Current colors")
    fabric: str = dspy.InputField(desc="Current fabric")
    occasion: str = dspy.InputField(desc="Current occasion level")
    trends: str = dspy.InputField(desc="Relevant fashion trends")

    advice: str = dspy.OutputField(
        desc="3-5 sentence personalized styling advice matching context"
    )
