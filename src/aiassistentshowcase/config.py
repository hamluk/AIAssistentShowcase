from pydantic import BaseModel


class AIAssistentShowcaseSettings(BaseModel):
    llm_mistral_model: str
    mistral_api_key: str

    active_model: str

    tavily_api_key: str