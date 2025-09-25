from abc import ABC, abstractmethod
from langchain_google_genai import ChatGoogleGenerativeAI
from models.schemas import AgentState
import os

class BaseAgent(ABC):
    def __init__(self):
        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
    
    @abstractmethod
    async def execute(self, state: AgentState) -> AgentState:
        pass