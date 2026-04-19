from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    user_input: Dict[str, float]

    predicted_price: float
    comparable_summary: str

    market_context: List[str]
    regulation_context: List[str]

    investment_goal: str
    risk_level: str

    reasoning: str
    recommendation: str
    final_report: str