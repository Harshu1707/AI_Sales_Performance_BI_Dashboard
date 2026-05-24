from __future__ import annotations

import os

from google import genai
from dotenv import load_dotenv

from services.data_service import executive_summary

# Load environment variables
load_dotenv()


def _model():
    """
    Initialize Gemini client
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(api_key=api_key)


def _fallback_insights(summary: dict) -> dict:
    """
    Local fallback insights if Gemini is unavailable
    """

    losses = ", ".join(
        item["product"]
        for item in summary["lossMakingProducts"][:3]
    )

    return {
        "source": "local-analytics",
        "insights": [
            {
                "title": "Profit Concentration",
                "body": (
                    f"{summary['bestRegion']} is the strongest profit region "
                    f"with ${summary['bestRegionProfit']:,.0f} in profit. "
                    f"Prioritize retention campaigns and inventory expansion there."
                ),
                "tag": "Region",
            },
            {
                "title": "Category Leader",
                "body": (
                    f"{summary['bestCategory']} is the highest-performing category "
                    f"with ${summary['bestCategoryProfit']:,.0f} in profit."
                ),
                "tag": "Category",
            },
            {
                "title": "Discount Impact",
                "body": (
                    f"Discount-to-profit correlation is "
                    f"{summary['discountProfitCorrelation']}. "
                    f"High discounting may be affecting margins."
                ),
                "tag": "Margin",
            },
            {
                "title": "Loss-Making Products",
                "body": (
                    f"Products needing review include: {losses}. "
                    f"Consider repricing or reducing discount dependency."
                ),
                "tag": "Products",
            },
        ],
    }


def generate_insights(df) -> dict:
    """
    Generate AI-powered business insights
    """

    summary = executive_summary(df)

    client = _model()

    # Fallback if Gemini key missing
    if not client:
        return _fallback_insights(summary)

    prompt = f"""
You are a senior retail business intelligence analyst.

Analyze the following retail sales summary and generate:

1. Executive business insights
2. Strategic recommendations
3. Profitability analysis
4. Growth opportunities
5. Risk observations

Keep the response professional, concise, and actionable.

Dataset Summary:
{summary}
"""

    try:

        response = client.models.generate_content(
            model=os.getenv(
                "GEMINI_MODEL",
                "gemini-3.5-flash"
            ),
            contents=prompt
        )

        return {
            "source": "gemini-3.5-flash",
            "narrative": response.text,
            "summary": summary,
        }

    except Exception as exc:

        fallback = _fallback_insights(summary)

        fallback["warning"] = (
            f"Gemini request failed: {exc}"
        )

        return fallback


def generate_chat_answer(
    df,
    question: str,
    history: list
) -> str:
    """
    AI chatbot for business questions
    """

    summary = executive_summary(df)

    client = _model()

    # Local fallback mode
    if not client:

        q = question.lower()

        if "category" in q and "profit" in q:
            return (
                f"{summary['bestCategory']} generated the "
                f"highest profit at "
                f"${summary['bestCategoryProfit']:,.0f}."
            )

        if "region" in q:
            return (
                f"{summary['bestRegion']} is currently "
                f"the top-performing region by profit."
            )

        if "discount" in q:
            return (
                f"Discount correlation with profit is "
                f"{summary['discountProfitCorrelation']}. "
                f"Large discounts may reduce profitability."
            )

        return (
            "Gemini API is not configured yet. "
            "Local analytics suggest focusing on profitable "
            "regions, reducing discount leakage, and reviewing "
            "loss-making products."
        )

    prompt = f"""
You are InsightIQ, an AI-powered executive business intelligence assistant.

Answer the user's question using ONLY the dataset summary provided.

Rules:
- Be concise
- Be professional
- Give business-focused recommendations
- Mention metrics when useful
- Avoid hallucinations

Dataset Summary:
{summary}

Recent Chat History:
{history[-6:]}

User Question:
{question}
"""

    try:

        response = client.models.generate_content(
            model=os.getenv(
                "GEMINI_MODEL",
                "gemini-3.5-flash"
            ),
            contents=prompt
        )

        return response.text

    except Exception as exc:

        return (
            f"I could not reach Gemini right now ({exc}). "
            f"Based on local analytics, "
            f"{summary['bestRegion']} leads in profitability and "
            f"{summary['bestCategory']} is the strongest category."
        )