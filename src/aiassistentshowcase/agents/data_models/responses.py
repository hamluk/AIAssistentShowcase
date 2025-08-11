from typing import Optional
from pydantic import BaseModel, Field

class AgentResponseModel(BaseModel):
    """Structured response from the agent"""

    response: str = Field(description="Final answer to the user's question")
    needs_escalation: bool
    follow_up_required: bool
    priority: str = Field(description="Priority of the request. Can be either 'low', 'medium', or 'high'")

class CustomerResponse(BaseModel):
    """Structured response for a request to retrieve customers from the database"""
    
    status_message: str = Field(description="""Structured response for a request to retrieve customers from the database""")
    customers: Optional[list] = None
