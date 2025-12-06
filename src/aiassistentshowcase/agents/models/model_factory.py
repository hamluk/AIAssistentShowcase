from aiassistentshowcase.agents.models.openai_model import init_openai_model_provider
from aiassistentshowcase.config import AIAssistentShowcaseSettings
from aiassistentshowcase.agents.models.mistral_model import init_mistral_model_provider


class ModelFactory:
    @staticmethod
    def get_model(settings: AIAssistentShowcaseSettings):
        if settings.active_model == "mistral":
            return init_mistral_model_provider(settings)
        elif settings.active_model == "openai":
            return init_openai_model_provider(settings)
        else:
            raise ValueError(settings.active_model)