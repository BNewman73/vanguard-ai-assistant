from langchain_core.messages import HumanMessage
from agent.graph.state import GraphState
from langgraph.types import interrupt

def hitl(state: GraphState):
  human_input = interrupt(state["draft"])
  decision = human_input["decision"]
  feedback = human_input.get("feedback", "")
  message = HumanMessage(content=decision)
  if decision == "revise":
    return {
      "messages": [HumanMessage(content=feedback)],
      "human_decision": "revise",
    }
  if decision == "approve":
    return {
      "messages": [message], 
      "human_decision": decision, 
    }
  # default to deny
  return {
    "messages": [message],
    "human_decision": "deny", 
    "final_response": "No action taken"
  }