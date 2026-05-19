
from langchain_core.messages import AIMessage, ToolMessage
import uuid
from agent.graph.state import GraphState


def create_action(tools: list):
  tool_map = {t.name: t for t in tools}
  async def action(state: GraphState):
    action_type = state["routing"].action_type
    tool = tool_map.get(action_type)
    if tool is None:
      result = f"No tool registered for action type: {action_type}"
      return {
        "messages":[AIMessage(content=f"No access to necessary tool for action_type: {action_type}")],  
        "final_response": "No action taken"}
    else:
      tool_call_id = str(uuid.uuid4())
      ai_message = AIMessage(
        content="",
        tool_calls=[{
          "id": tool_call_id,
          "name": tool.name,
          "args": state["draft"]
        }]
      )
      result = await tool.ainvoke(state["draft"])
      tool_message = ToolMessage(content=str(result[0]["text"]), tool_call_id=tool_call_id)
    return {
      "messages": [ai_message, tool_message],
      "final_response": result[0]["text"]
    }
  return action
