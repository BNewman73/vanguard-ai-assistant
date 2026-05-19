from operator import itemgetter
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.output_parsers import StrOutputParser
from langfuse import observe
from agent.graph.state import GraphState
from agent.utils.formatting import format_docs_with_sources


PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are the Vanguard Support Agent. Answer ONLY using the context below. Output ONLY a SupportDecision. "
        "If the answer is not in the context, answer should be python None. "
        "Otherwise, be sure to always cite the source document name(s)"
        "{summary_section}"
        "\n\nContext:\n{context}"
    )),
    ("human", "{question}"),
])

def create_support(llm, retriever: BaseRetriever):
  # @observe(name="support", as_type="generation")
  def support(state: GraphState):
    query = state["user_message"]
    summary = state.get("summary")
    summary_section = f"\n\nConversation Summary (prior context):\n{summary}" if summary else ""
    chain = (
        {
            "context": itemgetter("question") | retriever | format_docs_with_sources,
            "question": itemgetter("question"),
            "summary_section": itemgetter("summary_section"),
        }
        | PROMPT
        | llm
        | StrOutputParser()
    )
    result = chain.invoke({"question": query, "summary_section": summary_section})
    if not result.answer:
      # route to research as a fallback
      return {
        ""
      }
    return {
      "messages": [AIMessage(content=result)],
      "final_response": result
    }
  return support