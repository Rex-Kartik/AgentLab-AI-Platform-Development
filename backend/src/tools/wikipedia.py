import httpx
from pydantic import BaseModel, Field
from src.tools.interfaces import Tool, ToolUIConfig
from src.core.errors import ToolExecutionError

class WikipediaInput(BaseModel):
    query: str = Field(description="The search query for Wikipedia.")

class WikipediaTool(Tool):
    id = "wikipedia_query"
    name = "Wikipedia Query"
    description = "Searches Wikipedia for the given query and returns a summary."
    category = "knowledge"
    ui_config = ToolUIConfig(icon="library", accent_color="#8B5CF6")
    input_schema = WikipediaInput

    async def execute(self, query: str, **kwargs) -> str:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, follow_redirects=True, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("extract", "No summary found.")
                elif response.status_code == 404:
                    return f"Wikipedia page not found for '{query}'."
                else:
                    raise ToolExecutionError(self.id, f"Wikipedia API returned status code {response.status_code}")
            except Exception as e:
                raise ToolExecutionError(self.id, str(e))
