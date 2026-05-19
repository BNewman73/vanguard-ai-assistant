from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.state import RunnableConfig
from langgraph.types import Command
from agent.config import settings
import langgraph.config
import pprint
from agent.factories.llm import build_llm
from agent.factories.vectorstore import build_retriever
from agent.graph.models import RoutingDecision
from agent.graph.nodes.historian import create_historian
from agent.graph.nodes.hitl import hitl
from agent.graph.nodes.action import create_action
from agent.graph.nodes.coordinator import create_coordinator
from agent.graph.nodes.draft import create_draft
from agent.graph.nodes.research import create_research
from agent.graph.nodes.support import create_support
from agent.graph.routing import route, route_decision
from agent.graph.state import GraphState
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.checkpoint.memory import MemorySaver
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
import asyncio
import warnings
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer


def print_draft(payload: dict) -> None:
  width = 60
  print("\n" + "=" * width)
  print("  DRAFT FOR REVIEW")
  print("=" * width)
  for key, value in payload.items():
    label = key.replace("_", " ").upper()
    value_str = str(value)
    if "\n" in value_str or len(value_str) > width - len(label) - 4:
      print(f"  {label}:")
      for line in value_str.splitlines():
        print(f"    {line}")
    else:
      print(f"  {label}: {value_str}")
  print("=" * width)

def build_graph(coordinator_llm, subagent_llm, research_llm, retriever, research_tools, action_tools):
  builder = StateGraph(GraphState)

  builder.add_node("coordinator", create_coordinator(coordinator_llm))
  builder.add_node("historian", create_historian(subagent_llm))
  builder.add_node("support", create_support(subagent_llm, retriever))
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

# @observe(name="graph_turn")
async def invoke_turn(graph, user_message: str, config: RunnableConfig) -> str:
  result = await graph.ainvoke(
    {"user_message": user_message, "messages": [], "final_response": None},
    config,
  )
  while result.get("__interrupt__"):
    payload = result["__interrupt__"][0].value
    print_draft(payload)
    print("approve, deny, or revise?")
    choice = input("Your decision: ").strip().lower()

    if choice == "approve":
      resume_value = {"decision": "approve"}
    elif choice == "deny":
      resume_value = {"decision": "deny"}
    elif choice == "revise":
      feedback = input("Describe the changes: ").strip()
      resume_value = {"decision": "revise", "feedback": feedback}
      print("=" * 60)
    else:
      print("Unknown — defaulting to deny.")
      resume_value = {"decision": "deny"}

    result = await graph.ainvoke(Command(resume=resume_value), config=config)

    decision = graph.get_state(config).values.get("human_decision")
    if decision in ("approve", "deny"):
      break

  return result["final_response"]


async def main():
  warnings.filterwarnings("ignore", message="Pydantic serializer warnings")
  langfuse = Langfuse(
    public_key=settings.langfuse_public_key,
    secret_key=settings.langfuse_secret_key,
    host=settings.langfuse_base_url 
  )
  if langfuse.auth_check():
    print("Successfully authenticated!")
  langfuse_handler = CallbackHandler()
  client = MultiServerMCPClient(
    {"vanguard": {
      "command": "python",
      "args": ["-m", "agent.mcp_server.server"],
      "transport": "stdio",
    }}
  )
  async with client.session("vanguard") as session:
    tools = await load_mcp_tools(session)
    research_tools = [t for t in tools if t.name in {"web_search"}]
    action_tools   = [t for t in tools if t.name in {"send_email", "create_ticket", "log_action"}]

    coordinator_llm = build_llm().with_structured_output(RoutingDecision)
    subagent_llm = build_llm(max_tokens=2048)
    research_llm = subagent_llm.bind_tools(research_tools)
    retriever = build_retriever()

    graph = build_graph(coordinator_llm, subagent_llm, research_llm, retriever, research_tools, action_tools)
    config: RunnableConfig = {"configurable": {"thread_id": "capstone-thread-1"}, "callbacks": [langfuse_handler]}

    print("""
╔══════════════════════════════════════════════════════════════╗
║               Vanguard AI Assistant                          ║
╚══════════════════════════════════════════════════════════════╝

I can help you with:

  • Policy questions   — Ask anything about internal Vanguard
                         policies, procedures, or guidelines
  • Research           — Any question answered via live web search
  • Create a ticket    — Log a Jira issue (describe the problem)
  • Send an email      — Compose and send an email on your behalf
  • Log an action      — Record an action to the audit log

Type 'exit' or 'quit' to stop.
""")
    while True:
      try:
        user_message = input("You: ").strip()
      except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
        break

      if not user_message:
        continue
      if user_message.lower() in {"exit", "quit"}:
        print("Goodbye.")
        break

      response = await invoke_turn(graph, user_message, config)
      print(f"\nAgent: {response}\n")


if __name__ == "__main__":
  asyncio.run(main())
