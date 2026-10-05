from typing import Optional
from src.agent.interfaces import LLMProvider
from src.agent.provider_groq import GroqProvider

class ProviderFactory:
    @staticmethod
    def create(provider_name: str, model: str, api_key: Optional[str] = None) -> LLMProvider:
        # In ponytail fashion, since groq and openai use the exact same interface,
        # we can just use GroqProvider for both if we override base_url.
        # But Groq SDK doesn't easily expose base_url in AsyncGroq without custom httpx client.
        # For MVP, we will just pass it to GroqProvider which uses the groq SDK.
        
        if provider_name.lower() in ["groq", "openai"]:
            return GroqProvider(model=model, api_key=api_key)
        
        # Fallback to groq
        return GroqProvider(model=model, api_key=api_key)
