from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider
from aiassistentshowcase.config import AIAssistentShowcaseSettings


def init_mistral_model_provider(settings: AIAssistentShowcaseSettings):
    return MistralModel(settings.llm_model, provider=MistralProvider(api_key=settings.model_api_key))
