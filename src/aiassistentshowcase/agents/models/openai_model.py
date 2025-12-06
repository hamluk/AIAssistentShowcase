from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from aiassistentshowcase.config import AIAssistentShowcaseSettings


def init_openai_model_provider(settings: AIAssistentShowcaseSettings):
    return OpenAIChatModel(
        model_name=settings.llm_model,
        provider=OpenAIProvider(api_key=settings.model_api_key)
    )
