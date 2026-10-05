from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel

class AgentEvent(BaseModel):
    type: Literal[
        "agent.started",
        "agent.completed", 
        "tool.started", 
        "tool.completed", 
        "tool.failed",
        "agent.message"
    ]
    execution_id: str
    metadata: Dict[str, Any] = {}

class ToolStartedEvent(AgentEvent):
    type: Literal["tool.started"] = "tool.started"
    tool_id: str
    input: Dict[str, Any]

class ToolCompletedEvent(AgentEvent):
    type: Literal["tool.completed"] = "tool.completed"
    tool_id: str
    duration_ms: int
    output: Any

class ToolFailedEvent(AgentEvent):
    type: Literal["tool.failed"] = "tool.failed"
    tool_id: str
    error: str
