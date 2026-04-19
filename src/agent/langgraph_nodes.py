from src.rag.retriever import retrieve_context
from src.agent.llm import get_llm_response
from src.utils.cleaner import clean_text


def _extract_avg_price(comps: str):
    try:
        marker = "Avg Price: $"
        if marker not in comps:
            return None
        avg_part = comps.split(marker, 1)[1].split("\n", 1)[0]
        avg_part = avg_part.replace(",", "").strip()
        return float(avg_part)
    except Exception:
        return None


def _get_valuation_flag(price: float, comps: str) -> str:
    avg_price = _extract_avg_price(comps)
    if avg_price is None or avg_price <= 0:
        return "unknown"
    if price > avg_price * 1.2:
        return "overvalued"
    if price < avg_price * 0.8:
        return "undervalued"
    return "fair"


def retrieve_market_context_node(state):
    query = f"Property features: {state['user_input']}"
    context = retrieve_context(query)
    return {"market_context": context}


def analyze_property_node(state):
    valuation_flag = _get_valuation_flag(
        state["predicted_price"], state["comparable_summary"]
    )

    reasoning = (
        f"Predicted price analyzed against comparables. "
        f"Valuation signal: {valuation_flag}."
    )

    return {
        "reasoning": reasoning,
        "recommendation": valuation_flag,
    }


def generate_report_node(state):
    price = state["predicted_price"]
    comps = state["comparable_summary"]
    context = state.get("market_context", [])
    valuation_flag = state.get("recommendation", "unknown")

    prompt = f"""
You are a professional real estate investment advisor.

STRICT RULES:
- Use ONLY the given data.
- Do NOT hallucinate or invent missing facts.
- Be concise, realistic, and well-structured.
- Keep the output clean and readable.
- If evidence is weak, mention uncertainty.
- Recommendation must be one of: Buy / Wait / Caution.

INPUT DATA

Predicted Price:
{price}

Comparable Analysis:
{comps}

Market Context:
{context}

Valuation Signal:
{valuation_flag}

OUTPUT FORMAT (STRICT)

### Property Valuation
Estimated Price: $X

### Market Insights
- Point 1
- Point 2
- Point 3

### Comparable Analysis
- Summary of comparison
- Mention whether the property appears overvalued, undervalued, or fairly priced

### Recommendation
- Buy / Wait / Caution
- Clear reason

### Risks
- Risk 1
- Risk 2

### Disclaimer
General advisory only. Verify before investment.
"""

    try:
        response_text = get_llm_response(prompt)
        if not response_text or not str(response_text).strip():
            raise ValueError("LLM returned an empty advisory response.")
        response_text = clean_text(response_text)
    except Exception:
        context_points = context[:3] if context else [
            "Market context is limited because the LLM/API is unavailable right now."
        ]

        if valuation_flag == "overvalued":
            recommendation = "Caution"
            reason = "The predicted price appears above the comparable average."
            risks = [
                "There may be overvaluation risk relative to similar properties.",
                "Resale demand may not support the premium pricing."
            ]
        elif valuation_flag == "undervalued":
            recommendation = "Buy"
            reason = "The predicted price appears below the comparable average."
            risks = [
                "Hidden property issues may explain the lower valuation.",
                "Additional due diligence is required before treating it as a bargain."
            ]
        else:
            recommendation = "Wait"
            reason = "The property appears near fair value, so stronger evidence is needed."
            risks = [
                "Current evidence is not enough for a high-confidence investment decision.",
                "Market conditions may materially change the outcome."
            ]

        response_text = f"""
### Property Valuation
Estimated Price: ${price:,.0f}

### Market Insights
- {context_points[0]}
- {context_points[1] if len(context_points) > 1 else "Market trend evidence is limited in fallback mode."}
- {context_points[2] if len(context_points) > 2 else "Use live market checks before making a final decision."}

### Comparable Analysis
- {comps}
- Valuation signal: {valuation_flag}

### Recommendation
- {recommendation}
- {reason}

### Risks
- {risks[0]}
- {risks[1]}

### Disclaimer
General advisory only. This fallback report was generated without live LLM reasoning due to API limits or availability issues. Verify before investment.
"""
        response_text = clean_text(response_text)

    return {"final_report": response_text}