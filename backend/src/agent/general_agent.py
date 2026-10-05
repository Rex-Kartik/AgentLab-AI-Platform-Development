import time
import uuid
from typing import Any, Dict, List, AsyncGenerator
from src.agent.interfaces import Agent, LLMProvider
from src.agent.messages import BaseMessage, SystemMessage, UserMessage, ToolMessage
from src.agent.events import AgentEvent, ToolStartedEvent, ToolCompletedEvent, ToolFailedEvent
from src.tools.registry import ToolRegistry

class GeneralAgent(Agent):
    def __init__(self, provider: LLMProvider, registry: ToolRegistry):
        self.provider = provider
        self.registry = registry
        # Simplistic in-memory memory for MVP.
        # In a real app, this goes to ConversationRepository
        self.memory: Dict[str, List[BaseMessage]] = {}
        self.system_prompt = SystemMessage(
            content="You are AgentLab's General Agent, a powerful AI assistant with access to tools. "
                    "Use tools to answer questions or fetch real-time information. "
                    "CRITICAL: Communicate with the user in a natural, conversational human way. "
                    "DO NOT output raw markdown code, complex tables, or heavy formatting. Keep responses conversational and easy to read."
        )

    def get_available_tools(self) -> List[Dict[str, Any]]:
        return self.registry.get_all_schemas()

    async def execute(self, session_id: str, message: str, context_messages: List[Dict[str, Any]] = None) -> AsyncGenerator[AgentEvent, None]:
        # Stateless Ponytail approach: If frontend sends context (RAG/history), we use it.
        # Otherwise fallback to in-memory dict.
        messages_list = [self.system_prompt]
        
        if context_messages:
            from src.agent.messages import AssistantMessage
            for msg in context_messages:
                if msg.get("role") == "user":
                    messages_list.append(UserMessage(content=msg.get("content", "")))
                elif msg.get("role") == "assistant":
                    messages_list.append(AssistantMessage(content=msg.get("content", "")))
        elif session_id in self.memory:
            # Skip the system prompt which is already in memory
            messages_list = self.memory[session_id]
            
        messages_list.append(UserMessage(content=message))
        self.memory[session_id] = messages_list
        
        execution_id = str(uuid.uuid4())
        yield AgentEvent(type="agent.started", execution_id=execution_id)
        
        while True:
            tools = self.get_available_tools()
            response = await self.provider.generate_response(self.memory[session_id], tools)
            self.memory[session_id].append(response)

            # If no tool calls, we are done
            if not response.tool_calls:
                yield AgentEvent(
                    type="agent.completed", 
                    execution_id=execution_id, 
                    metadata={"content": response.content}
                )
                break
                
            # Execute tool calls
            for tool_call in response.tool_calls:
                tool_id = tool_call.function["name"]
                args = tool_call.function["arguments"]
                
                yield ToolStartedEvent(
                    execution_id=execution_id,
                    tool_id=tool_id,
                    input=args
                )
                
                start_time = time.time()
                try:
                    tool = self.registry.get_tool(tool_id)
                    result = await tool.execute(**args)
                    duration = int((time.time() - start_time) * 1000)
                    
                    yield ToolCompletedEvent(
                        execution_id=execution_id,
                        tool_id=tool_id,
                        duration_ms=duration,
                        output=result
                    )
                    
                    self.memory[session_id].append(ToolMessage(
                        tool_call_id=tool_call.id,
                        name=tool_id,
                        content=str(result)
                    ))
                except Exception as e:
                    yield ToolFailedEvent(
                        execution_id=execution_id,
                        tool_id=tool_id,
                        error=str(e)
                    )
                    self.memory[session_id].append(ToolMessage(
                        tool_call_id=tool_call.id,
                        name=tool_id,
                        content=f"Error executing tool: {str(e)}"
                    ))
                    
        # loop continues to let the LLM see the tool output and respond
