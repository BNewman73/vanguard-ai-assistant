from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_core.language_models import BaseChatModel
from langchain_openai import AzureChatOpenAI

from agent.config import settings

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

def build_llm(provider: str = settings.default_llm_provider, temp: float = settings.default_temp, max_tokens: int = 1024) -> BaseChatModel:
  match provider:
    case "azure_openai":
      return AzureChatOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        azure_deployment=settings.azure_openai_deployment,
        api_version=settings.azure_openai_api_version,
        azure_ad_token_provider=token_provider,
        temperature=temp,
        max_completion_tokens=max_tokens
    )
    case _:
      raise ValueError(f"Unsupported LLM provider: {provider}")
