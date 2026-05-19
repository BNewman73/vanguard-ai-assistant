from langchain_core.messages import HumanMessage, SystemMessage
from agent.graph.state import GraphState
import uuid

SYSTEM_PROMPT = """
You are a routing coordinator. Your ONLY job is to decide which agent should handle the user message. Output ONLY a RoutingDecision. No prose.

Agents available:
  "support"  — questions answerable from Vanguard documents: fund facts, expense ratios, fees, policies, account procedures, FAQs
  "research" — requires live or real-time data: current prices, recent news, market data not found in documents
  "draft"   — perform an action: send email, create ticket, log something
""".strip()

def create_coordinator(llm):
  # @observe(name="coordinator", as_type="generation")
  def coordinator(state: GraphState):
    # query = HumanMessage(content=state["user_message"], id=str(uuid.uuid4()))
    query = state["messages"][-1]
    messages = [SystemMessage(SYSTEM_PROMPT), query]
    result = llm.invoke(messages)
    content = query.content
    if isinstance(content, list):
      content = " ".join(block["text"] for block in content if block.get("type") == "text")
    return {
      # "messages": [query],
      "user_message": content,
      "query_ids": query.id,
      "routing": result,
      "final_response": None
   }
  return coordinator
