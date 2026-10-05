from abc import ABC, abstractmethod
from typing import Any, Dict, List, AsyncGenerator
from .messages import BaseMessage
from src.tools.registry import ToolRegistry

class LLMProvider(ABC):
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[BaseMessage], 
        tools: List[Dict[str, Any]] = None
    ) -> BaseMessage:
        pass

class Agent(ABC):
    @abstractmethod
    async def execute(self, session_id: str, message: str) -> AsyncGenerator[Any, None]:
        """Executes the agent workflow and yields typed events."""
        pass
    
    @abstractmethod
    def get_available_tools(self) -> List[Dict[str, Any]]:
        pass
