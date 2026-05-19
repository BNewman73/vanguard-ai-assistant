from pathlib import Path
from langchain_community.document_loaders import (
  PyPDFLoader,
  BSHTMLLoader,
  TextLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from agent.factories.vectorstore import build_embeddings, build_vectorstore
from agent.config import settings
from langchain_core.documents import Document

if __name__ == "__main__":
  splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base",
    chunk_size=512,
    chunk_overlap=50,
    separators=[
      "\n============================================================\n",
      "\n------------------------------------------------------------\n",
      "\n\n", "\n", ". ", " ", ""
    ],
  )
  KB = Path("./knowledge_base")
  docs = []
  chunked_docs = []

  for pdf in KB.glob("*.pdf"):
    pages = PyPDFLoader(str(pdf)).load()
    full_text = " ".join(p.page_content for p in pages)
    # build character offset map
    page_map = []
    pos = 0
    for p in pages:
      end = pos + len(p.page_content)
      page_map.append((pos, end, p.metadata["page"]))
      pos = end + 1  # account for " " from join
    pdf_chunks = splitter.split_text(full_text)
    for chunk in pdf_chunks:
      pos = full_text.find(chunk)
      page = next(pg for (s, e, pg) in page_map if s <= pos <= e)
      chunked_docs.append(Document(
          page_content=chunk,
          metadata={"source": str(pdf), "page": page}
      ))

  for md in KB.glob("*.md"):
    docs.extend(TextLoader(str(md)).load())

  for html in KB.glob("*.html"):
    docs.extend(BSHTMLLoader(str(html)).load())

  split_non_pdf = splitter.split_documents(docs)
  chunked_docs.extend(split_non_pdf)

  embeddings = build_embeddings()
  vectorstore = build_vectorstore(embeddings)
  vectorstore.add_documents(chunked_docs)

  pdf_chunk_count = len(chunked_docs) - len(split_non_pdf)
  print(f"Loaded {pdf_chunk_count} pdf chunks")
  print(f"Loaded {len(split_non_pdf)} other chunks (from {len(docs)} files)")
  print(f"Stored {len(chunked_docs)} total chunks")


  