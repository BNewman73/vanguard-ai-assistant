from langchain_core.documents import Document

def format_docs_with_sources(docs: list[Document]) -> str:
    """Format retrieved chunks into a single LLM-ready context string.

    Prefixes each chunk with its source filename and section header so
    the model can cite them. Chunks are joined with `---` separators —
    empirically, LLMs handle these better than bare concatenation
    because the visual break signals "new source, new topic".
    """
    parts: list[str] = []
    for doc in docs:
      source = doc.metadata.get("source", "unknown")
      parts.append(f"[Source: {source}]\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def print_query_result(
    question: str,
    docs: list[Document],
    answer: str,
    *,
    preview_chars: int = 90,
) -> None:
    """Pretty-print a single RAG cycle: question, sources, answer."""
    banner = "=" * 70
    print(f"\n{banner}")
    print(f"Q: {question}")
    print(banner)

    print(f"\nRetrieved {len(docs)} chunks:")
    for i, doc in enumerate(docs, 1):
      source = doc.metadata.get("source", "unknown")
      section = doc.metadata.get("section", "General")
      preview = doc.page_content[:preview_chars].replace("\n", " ")
      print(f"  {i}. [{source} | {section}] {preview}...")

    print(f"\nA: {answer}\n")