from aiassistentshowcase.agents.data_models.responses import AgentResponseModel, CustomerResponse 
from aiassistentshowcase.agents.data_models.dependencies import DBDependencies
from aiassistentshowcase.agents.prompts.system_prompts import system_customer_assistent_prompt
from aiassistentshowcase.agents.tools.tavily_search import create_tool_set
from aiassistentshowcase.config import AIAssistentShowcaseSettings
from aiassistentshowcase.agents.models import ModelFactory
from pydantic_ai import Agent, RunContext


class ActionAgent():
    def __init__(self, settings: AIAssistentShowcaseSettings):
        self.settings = settings
        self.agent = self._init_agent()
    
    def _init_agent(self) -> Agent:
        agent = Agent(
            model = ModelFactory.get_model(settings=self.settings),
            tools = create_tool_set(settings=self.settings),
            output_type=[AgentResponseModel],
            system_prompt=system_customer_assistent_prompt
            )

        @agent.tool
        def list_all_customers_tool(ctx: RunContext[DBDependencies]):
            if ctx.deps is None:
                raise ValueError("Dependencies (ctx.deps) wurden nicht gesetzt.")
            
            db = ctx.deps.db
            customers = db.list_all_customer()
            return f"{customers}"
        
        return agent

    def run(self, query: str, deps) -> str:
        try:
            result = self.agent.run_sync(user_prompt=query, deps=deps)
            return result.output.__dict__["response"]
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
