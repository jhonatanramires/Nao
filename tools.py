from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.pydantic_v1 import BaseModel

import os

os.environ["TAVILY_API_KEY"] = "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"

tool = TavilySearchResults(max_results=2)



class RequestAssistance(BaseModel):
    """Escalate the conversation to an expert. Use this if you are unable to assist directly or if the user requires support beyond your permissions.

    To use this function, relay the user's 'request' so the expert can provide the right guidance.
    """

    request: str

class RequestAproval(BaseModel):
    """in some sort of actions you need aproval to do them describe shortly what you want to do and why"""

    request: str

tools = [tool,RequestAssistance,RequestAproval]
