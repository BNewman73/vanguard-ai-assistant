from agent.graph.state import GraphState

def route(state: GraphState):
  if state["routing"] is None:
    raise ValueError("route() called before coordinator set routing")
  return state["routing"].agent


def route_decision(state: GraphState):
  decision = state["human_decision"]
  if decision is None:
    raise ValueError("human_decision not set")
  return decision