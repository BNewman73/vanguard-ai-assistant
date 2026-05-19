# agent/graph/factory.py
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.graph.state import CompiledStateGraph
from agent.factories.llm import build_llm
from agent.factories.vectorstore import build_retriever
from agent.graph.models import RoutingDecision, SupportResult
from agent.graph.nodes.action import create_action
from agent.graph.nodes.coordinator import create_coordinator
from agent.graph.nodes.draft import create_draft
from agent.graph.nodes.historian import create_historian
from agent.graph.nodes.hitl import hitl
from agent.graph.nodes.research import create_research
from agent.graph.nodes.support import create_support
from agent.graph.state import GraphState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from agent.graph.routing import route, route_decision

# Import your static tool definitions directly (no MCP session needed)
from agent.mcp_server.server import web_search, send_email, create_ticket, log_action

def make_graph(config: RunnableConfig) -> CompiledStateGraph:
  research_tools = [tool(web_search)]
  action_tools = [tool(send_email), tool(create_ticket), tool(log_action)]

  coordinator_llm = build_llm().with_structured_output(RoutingDecision)
  support_llm = build_llm(max_tokens=2048).with_structured_output(SupportResult)
  subagent_llm = build_llm(max_tokens=2048)
  research_llm = subagent_llm.bind_tools(research_tools)
  retriever = build_retriever()

  builder = StateGraph(GraphState)
  builder.add_node("coordinator", create_coordinator(coordinator_llm))
  builder.add_node("historian", create_historian(subagent_llm))
  builder.add_node("support", create_support(support_llm, retriever))
  builder.add_node("research", create_research(research_llm))
  builder.add_node("draft", create_draft(subagent_llm))
  builder.add_node("hitl", hitl)
  builder.add_node("action", create_action(action_tools))
  builder.add_node("research_tools", ToolNode(research_tools))

  builder.set_entry_point("coordinator")
  builder.add_edge("coordinator", "historian")
  builder.add_conditional_edges("historian", route)
  builder.add_edge("draft", "hitl")
  builder.add_conditional_edges("hitl", route_decision, {"approve": "action", "deny": END, "revise": "draft"})
  builder.add_conditional_edges("research", tools_condition, {"tools": "research_tools", "__end__": END})
  builder.add_edge("action", END)
  builder.add_edge("research_tools", "research")
  builder.add_edge("support", END)

  serde = JsonPlusSerializer(allowed_msgpack_modules=[RoutingDecision])
  return builder.compile(checkpointer=MemorySaver(serde=serde))