import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from src.api.schemas import ChatRequest, ToolMetadataResponse
from src.tools.registry import registry
from src.agent.general_agent import GeneralAgent
from src.agent.provider_groq import GroqProvider

router = APIRouter()
    
@router.get("/tools", response_model=list[ToolMetadataResponse])
async def get_tools():
    """Returns available tools and their UI metadata."""
    return registry.get_ui_metadata()

# Removed Depends(get_agent) because we create it dynamically now
@router.post("/chat")
async def chat_stream(request: ChatRequest):
    """Streams agent execution events to the frontend."""
    from src.agent.provider_factory import ProviderFactory
    provider = ProviderFactory.create(request.provider, request.model, request.api_key)
    agent = GeneralAgent(provider=provider, registry=registry)
    
    async def event_generator():
        try:
            async for event in agent.execute(request.session_id, request.message, request.context_messages):
                yield f"data: {event.model_dump_json()}\n\n"
        except Exception as e:
            from src.agent.events import ToolExecutionEvent
            import time
            import uuid
            # Fallback error event if something explodes outside tool execution
            yield f"data: {{\"type\": \"agent.error\", \"error\": \"{str(e)}\"}}\n\n"
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")
