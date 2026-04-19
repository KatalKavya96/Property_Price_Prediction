from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState
from src.agent.langgraph_nodes import (
    retrieve_market_context_node,
    analyze_property_node,
    generate_report_node,
)


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("retrieve_market_context", retrieve_market_context_node)
    graph.add_node("analyze_property", analyze_property_node)
    graph.add_node("generate_report", generate_report_node)

    graph.add_edge(START, "retrieve_market_context")
    graph.add_edge("retrieve_market_context", "analyze_property")
    graph.add_edge("analyze_property", "generate_report")
    graph.add_edge("generate_report", END)

    return graph.compile()