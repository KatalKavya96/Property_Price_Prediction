import html
import streamlit as st


SECTION_ORDER = [
    "Property Valuation",
    "Market Insights",
    "Comparable Analysis",
    "Recommendation",
    "Risks",
    "Disclaimer",
]


def parse_advisory_sections(report: str) -> dict:
    sections = {key: "" for key in SECTION_ORDER}

    current = None
    for raw_line in report.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("### "):
            title = line.replace("### ", "").strip()
            if title in sections:
                current = title
            continue

        if current:
            sections[current] += line + "\n"

    return {k: v.strip() for k, v in sections.items()}


def _render_small_card(title: str, body: str):
    safe_title = html.escape(title)
    safe_body = html.escape(body or "Not available").replace("\n", "<br>")
    st.markdown(
        f"""
<div class="card advisory-card">
  <div class="section-title">{safe_title}</div>
  <div class="section-body">{safe_body}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _render_evidence_block(latest_price, comparables, context_points):
    price_text = f"${latest_price:,.0f}" if latest_price is not None else "Not available"
    comp_text = comparables or "Comparable analysis not available."
    safe_comp = html.escape(comp_text).replace("\n", "<br>")

    if not context_points:
        context_points = ["No retrieved market context available."]

    bullets = "".join(
        f"<li>{html.escape(point)}</li>" for point in context_points[:5]
    )

    st.markdown(
        f"""
<div class="card evidence-card">
  <div class="section-title">Evidence Used</div>
  <div class="evidence-grid">
    <div class="evidence-pill">
      <div class="evidence-label">Predicted Price</div>
      <div class="evidence-value">{price_text}</div>
    </div>
  </div>
  <div class="evidence-subtitle">Comparable Analysis</div>
  <div class="section-body">{safe_comp}</div>
  <div class="evidence-subtitle">Retrieved Market Context</div>
  <ul class="evidence-list">
    {bullets}
  </ul>
</div>
""",
        unsafe_allow_html=True,
    )


def render_advisory(report: str, comparables: str = None, context_points=None, latest_price=None):
    context_points = context_points or []
    sections = parse_advisory_sections(report)

    st.markdown(
        """
<div class="card advisory-hero">
  <div class="h1">AI Investment Advisory</div>
  <div class="sub">ML + comparables + RAG + LangGraph reasoning</div>
</div>
""",
        unsafe_allow_html=True,
    )

    _render_evidence_block(
        latest_price=latest_price,
        comparables=comparables,
        context_points=context_points,
    )

    c1, c2 = st.columns(2, gap="medium")

    with c1:
        _render_small_card("Property Valuation", sections["Property Valuation"])
        _render_small_card("Comparable Analysis", sections["Comparable Analysis"])
        _render_small_card("Risks", sections["Risks"])

    with c2:
        _render_small_card("Market Insights", sections["Market Insights"])
        _render_small_card("Recommendation", sections["Recommendation"])
        _render_small_card("Disclaimer", sections["Disclaimer"])