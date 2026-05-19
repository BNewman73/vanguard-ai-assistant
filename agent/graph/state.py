from typing import Annotated, Literal, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from agent.graph.models import RoutingDecision

def query_ids_reducer(existing: list[str], new) -> list[str]:
  if isinstance(new, list):
    return new
  if not existing:
    existing = []
  return existing + [new]

class GraphState(TypedDict):
  user_message: str                              
  messages: Annotated[list[BaseMessage], add_messages]
  query_ids: Annotated[list[str], query_ids_reducer]
  summary: str
  summary_turn_count: int
  routing: RoutingDecision # set by coordinator (Pydantic model)
  draft: dict
  human_decision: Literal["approve", "deny", "revise"]
  # retrieved_chunks: list[RetrievedChunk]     # set by RAG step
  # tool_results: list[ToolResult]             # set by tool nodes
  final_response: str | None                   # set by subagent