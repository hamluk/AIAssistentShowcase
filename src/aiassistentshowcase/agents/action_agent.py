from aiassistentshowcase.agents.data_models.responses import AgentResponseModel, CustomerResponse 
from aiassistentshowcase.agents.data_models.dependencies import DBDependencies
from aiassistentshowcase.agents.prompts.system_prompts import system_customer_assistent_prompt
from aiassistentshowcase.agents.tools.tavily_search import create_tool_set
from aiassistentshowcase.config import AIAssistentShowcaseSettings
from aiassistentshowcase.agents.models import ModelFactory
from pydantic_ai import Agent, RunContext

import json


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

        # @agent.tool
        # def list_all_customers_tool(ctx: RunContext[DBDependencies]):
        #     if ctx.deps is None:
        #         raise ValueError("Dependencies (ctx.deps) wurden nicht gesetzt.")
            
        #     db = ctx.deps.db
        #     customers = db.list_all_customer()
        #     return f"{customers}"
        
        # @agent.tool
        # def create_new_customer_tool(ctx: RunContext[DBDependencies], firstname: str, lastname: str, age: int, priority: int, note: str):
        #     if ctx.deps is None:
        #         raise ValueError("Dependencies (ctx.deps) not set!")
            
        #     db = ctx.deps.db
        #     success_message = db.create_new_customer(firstname=firstname, lastname=lastname, age=age, priority=priority, note=note)
        #     return success_message
        
        return agent

    def run(self, query: str) -> str:
        print("Query: ", query)
        try:
            result = self.agent.run_sync(query)
            print("Answer received")
            result_all_json = json.loads(result.all_messages_json())
            print(json.dumps(result_all_json, indent=4))
            print(" ----- END OF ALL MESAGES ---- ")
            print("------ AI Agent response: ------\n")
            print(json.dumps(result.output.__dict__, indent=4))
            return result.output.__dict__["response"]
        except Exception as e:
            print("Error during agent run:", e)
            return f"An error occurred: {str(e)}"
        
