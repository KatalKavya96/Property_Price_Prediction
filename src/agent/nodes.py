from src.agent.graph import build_agent_graph

graph_app = build_agent_graph()


def run_agent(state, dataset):
    result = graph_app.invoke(state)
    return result