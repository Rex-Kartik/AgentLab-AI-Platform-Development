from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class ChatRequest(BaseModel):
    session_id: str
    message: str
    provider: str = "groq"
    model: str = "openai/gpt-oss-120b"
    api_key: Optional[str] = None
    context_messages: Optional[List[Dict[str, Any]]] = None

class ToolMetadataResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    icon: str
    accentColor: str
