from pydantic_ai.common_tools.tavily import tavily_search_tool
from aiassistentshowcase.config import AIAssistentShowcaseSettings

def create_tool_set(settings: AIAssistentShowcaseSettings) -> list:
    tool_set = []
    tool_set.append(tavily_search_tool(settings.tavily_api_key))
    return tool_set