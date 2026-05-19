from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
  # LLM
  default_llm_provider: str
  default_temp: float
  azure_openai_endpoint: str
  azure_openai_deployment: str
  azure_openai_api_version: str
  # Embeddings
  embedding_provider: str
  embedding_model: str
  # Vector Store
  vector_store_backend: str
  chroma_persist_dir: str
  chroma_collection_name: str
  # MCP
  tavily_api_key: str
  sg_api_key: str
  sg_from_email: str
  # LangFuse
  langfuse_secret_key: str
  langfuse_public_key: str
  langfuse_base_url: str
  # LangSmith
  langsmith_api_key: str
  # Context History Management
  trim_threshold: int = 2
  turns_to_keep: int = 1

  model_config = SettingsConfigDict(env_file=".env")

settings = AppConfig()