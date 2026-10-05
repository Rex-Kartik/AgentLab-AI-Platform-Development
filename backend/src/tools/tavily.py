import httpx
from pydantic import BaseModel, Field
from src.tools.interfaces import Tool, ToolUIConfig
from src.core.config import settings
from src.core.errors import ToolExecutionError

class TavilyInput(BaseModel):
    query: str = Field(description="The search query to find information on the web.")

class TavilyTool(Tool):
    id = "tavily_search"
    name = "Tavily Search"
    description = "Searches the web in real-time for up-to-date information."
    category = "search"
    ui_config = ToolUIConfig(icon="search", accent_color="#60A5FA")
    input_schema = TavilyInput

    async def execute(self, query: str, **kwargs) -> str:
        api_key = settings.TAVILY_API_KEY
        if not api_key or api_key == "placeholder_for_tavily_api_key":
            return "Tavily API key not configured. Mock search result for: " + query

        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": 3
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=15.0)
                if response.status_code == 200:
                    results = response.json().get("results", [])
                    return "\n\n".join([f"{r['title']}: {r['content']}" for r in results])
                else:
                    raise ToolExecutionError(self.id, f"Tavily API returned status code {response.status_code}")
            except Exception as e:
                raise ToolExecutionError(self.id, str(e))
