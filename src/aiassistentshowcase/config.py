from pydantic import BaseModel


class AIAssistentShowcaseSettings(BaseModel):
    llm_model: str
    model_api_key: str

    active_model: str

    tavily_api_key: str