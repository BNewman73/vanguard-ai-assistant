from langchain_core.messages import BaseMessage, HumanMessage, RemoveMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from agent.graph.state import GraphState
from agent.config import settings

PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are responsible for summarizing trimmed message history by extending the existing running summary. "
        "Append one line per turn in the format 'Turn N: <summary>' where N continues from the existing summary and starting at 0. "
        "A turn starts with a human message and ends with a final ai message and consists of these with all the messages in between. "
        "The start of each turn will be presented to you with 'Start Turn'. "
        "Output the full updated summary - this includes the existing summary appended with your additional lines per new turn presented to you. "
        # "First new turn number is {start_turn_num}. 
        "\n\nExisting Summary:\n{summary}"
    )),
    ("human", "{formatted_turns}"),
])

def create_historian(llm):
  def historian(state: GraphState):
    query_ids = state["query_ids"]
    num_turns = len(query_ids) - 1
    if num_turns >= settings.trim_threshold:
      i = num_turns - settings.turns_to_keep 
      kept_query_ids = query_ids[i:]
      trimmed_messages = trim_messages(state["messages"], query_ids[i])
      trimmed_query_ids = query_ids[:i]
      formatted_turns = format_turns(trimmed_messages, trimmed_query_ids)
      # current_turn_count = state.get("summary_turn_count", 0)
      # num_new_turns = len(trimmed_query_ids) - 1
      input = {
        "summary": state.get("summary", ""),
        "formatted_turns": formatted_turns,
        # "start_turn_num": current_turn_count + 1,
      }
      chain = PROMPT | llm | StrOutputParser()
      response = chain.invoke(input)
      messages_to_remove = [RemoveMessage(id=msg.id) for msg in trimmed_messages]
      return {
        "messages": messages_to_remove,
        "summary": response,
        "query_ids": kept_query_ids,
        # "summary_turn_count": current_turn_count + num_new_turns,
      }
    return {}
  return historian

def trim_messages(messages: list[BaseMessage], id) -> list[BaseMessage]:
  index = next(
    (i for i, msg in enumerate(messages) if msg.id == id),
    None
)
  if index is None:
      raise ValueError(f"No message found with id {id}")
  trimmed_messages = messages[:index]
  return trimmed_messages


def format_turns(messages: list[BaseMessage], trimmed_query_ids) -> str:
  turns = []
  start = 0
  i = 0
  for id in trimmed_query_ids[1:]:
    while i < len(messages):
      message = messages[i]
      if id == message.id:
        turns.append(messages[start:i])
        start = i
        i = i + 1
        break
      i = i + 1
  turns.append(messages[start:]) 
  return "\n".join(format_turn(turn) for turn in turns)

def format_turn(messages: list[BaseMessage]) -> str:
  return "Start Turn:\n" + "\n".join(format_message(m) for m in messages) + "\n"

def extract_text(content) -> str:
  if isinstance(content, list):
    return " ".join(block["text"] for block in content if block.get("type") == "text")
  return content

def format_message(message: BaseMessage) -> str:
  match message:
    case HumanMessage():
      return f"Human: {extract_text(message.content)}"
    case AIMessage():
      parts = []
      if message.content:
        parts.append(f"AI: {extract_text(message.content)}")
      for tc in message.tool_calls:
        parts.append(f"AI (tool call with id {tc['id']}): {tc['name']}({tc['args']})")
      return "\n".join(parts)
    case ToolMessage():
      return f"Tool result of tool call with id {message.tool_call_id}: {extract_text(message.content)}"
    case _:
      raise ValueError(f"Unknown message type: {type(message)}")