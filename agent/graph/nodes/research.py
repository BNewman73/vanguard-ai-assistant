from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from agent.graph.state import GraphState


PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are the Vanguard Research Agent. Answer using your provided tools as necessary. "
        "If you are unsure of the answer, say so explicitly. "
        "Otherwise, always cite the source of your relevant web findings at the end of your answer."
        "{summary_section}"
    )),
    MessagesPlaceholder("messages"),
])

def create_research(llm):
  # @observe(name="research", as_type="generation")
  def research(state: GraphState):
    summary = state.get("summary")
    summary_section = f"\n\nConversation Summary (prior context):\n{summary}" if summary else ""
    response = (PROMPT | llm).invoke({"messages": state["messages"], "summary_section": summary_section})
    return {
      "messages": [response],
      "final_response": response.content if response.content else None
    }
  return research