import json
from typing import Any, Dict, List
from groq import AsyncGroq
from src.agent.interfaces import LLMProvider
from src.agent.messages import BaseMessage, SystemMessage, UserMessage, AssistantMessage, ToolMessage, ToolCall
from src.core.config import settings
from src.core.errors import LLMProviderError

class GroqProvider(LLMProvider):
    def __init__(self, model: str = "openai/gpt-oss-120b", api_key: str = None):
        self.model = model
        self.api_key = api_key or settings.GROQ_API_KEY
        if not self.api_key or self.api_key == "placeholder_for_groq_api_key":
            print("WARNING: Groq API key not set, using placeholder. API calls will fail.")
        self.client = AsyncGroq(api_key=self.api_key)

    def _convert_messages(self, messages: List[BaseMessage]) -> List[Dict[str, Any]]:
        result = []
        for msg in messages:
            if isinstance(msg, SystemMessage) or isinstance(msg, UserMessage):
                result.append({"role": msg.role, "content": msg.content})
            elif isinstance(msg, ToolMessage):
                result.append({
                    "role": "tool",
                    "content": msg.content,
                    "tool_call_id": msg.tool_call_id,
                    "name": msg.name
                })
            elif isinstance(msg, AssistantMessage):
                msg_dict = {"role": "assistant"}
                if msg.content:
                    msg_dict["content"] = msg.content
                if msg.tool_calls:
                    msg_dict["tool_calls"] = [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function["name"],
                                "arguments": json.dumps(tc.function["arguments"])
                            }
                        }
                        for tc in msg.tool_calls
                    ]
                result.append(msg_dict)
        return result

    async def generate_response(
        self, 
        messages: List[BaseMessage], 
        tools: List[Dict[str, Any]] = None
    ) -> AssistantMessage:
        groq_messages = self._convert_messages(messages)
        kwargs = {
            "model": self.model,
            "messages": groq_messages,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        try:
            response = await self.client.chat.completions.create(**kwargs)
            message = response.choices[0].message
            
            tool_calls = None
            if message.tool_calls:
                tool_calls = [
                    ToolCall(
                        id=tc.id,
                        function={
                            "name": tc.function.name,
                            "arguments": json.loads(tc.function.arguments)
                        }
                    )
                    for tc in message.tool_calls
                ]
                
            return AssistantMessage(
                content=message.content,
                tool_calls=tool_calls
            )
        except Exception as e:
            raise LLMProviderError(f"Groq API error: {str(e)}")
