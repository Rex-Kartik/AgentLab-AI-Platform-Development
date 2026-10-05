from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field

class BaseMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: Optional[str] = None

class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"

class UserMessage(BaseMessage):
    role: Literal["user"] = "user"

class ToolCall(BaseModel):
    id: str
    type: Literal["function"] = "function"
    function: Dict[str, Any]  # name, arguments

class AssistantMessage(BaseMessage):
    role: Literal["assistant"] = "assistant"
    tool_calls: Optional[List[ToolCall]] = None

class ToolMessage(BaseMessage):
    role: Literal["tool"] = "tool"
    tool_call_id: str
    name: str
