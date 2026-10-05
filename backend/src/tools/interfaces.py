from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel

class ToolUIConfig(BaseModel):
    icon: str
    accent_color: str

class Tool(ABC):
    id: str
    name: str
    description: str
    version: str = "1.0.0"
    category: str
    ui_config: ToolUIConfig
    input_schema: Type[BaseModel]

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        pass

    def get_schema(self) -> Dict[str, Any]:
        """Returns OpenAI/Groq compatible tool schema."""
        return {
            "type": "function",
            "function": {
                "name": self.id,
                "description": self.description,
                "parameters": self.input_schema.model_json_schema()
            }
        }
