class AgentLabError(Exception):
    """Base error for all AgentLab exceptions."""
    pass

class ToolExecutionError(AgentLabError):
    """Raised when a tool fails to execute properly."""
    def __init__(self, tool_id: str, message: str):
        super().__init__(f"Tool '{tool_id}' failed: {message}")
        self.tool_id = tool_id
        self.message = message

class LLMProviderError(AgentLabError):
    """Raised when an LLM provider fails."""
    pass

class ToolNotFoundError(AgentLabError):
    """Raised when attempting to use an unregistered tool."""
    pass
