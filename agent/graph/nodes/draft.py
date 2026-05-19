from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from agent.graph.models import ACTION_MODELS
from agent.graph.state import GraphState

PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are the Vanguard Action Agent. Create a draft for the requested action."
        "{summary_section}"
    )),
    MessagesPlaceholder("messages"),
])

def create_draft(llm: BaseChatModel):
  def draft(state: GraphState):
    summary = state.get("summary")
    summary_section = f"\n\nConversation Summary (prior context):\n{summary}" if summary else ""
    model = ACTION_MODELS[state["routing"].action_type]
    result = (PROMPT | llm.with_structured_output(model, include_raw=True)).invoke(
        {"messages": state["messages"], "summary_section": summary_section}
    )
    return {
      "draft": result["parsed"].model_dump(),
      "messages": [result["raw"]]
    }
  return draft