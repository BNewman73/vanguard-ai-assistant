from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from agent.config import settings

def build_embeddings() -> Embeddings:
  match settings.embedding_provider:
    case "huggingface":
      return HuggingFaceEmbeddings(model=settings.embedding_model)
    case _:
      raise ValueError(f"Unsupported embedding provider: {settings.embedding_provider}")

def build_vectorstore(embeddings = None) -> VectorStore:
  if not embeddings:
    embeddings = build_embeddings()
  match settings.vector_store_backend:
    case "chroma":
      return Chroma(collection_name=settings.chroma_collection_name, embedding_function=embeddings, persist_directory=settings.chroma_persist_dir)
    case _:
      raise ValueError(f"Unsupported vector store backend: {settings.vector_store_backend}")

def build_retriever(vectorstore = None) -> BaseRetriever:
    if vectorstore is None:
      vectorstore = build_vectorstore()
    return vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})
