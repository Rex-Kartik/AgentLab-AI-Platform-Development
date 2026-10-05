from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.tools.registry import registry
from src.tools.wikipedia import WikipediaTool
from src.tools.tavily import TavilyTool
from src.tools.math_tools import AddTool, MultiplyTool

def create_app() -> FastAPI:
    app = FastAPI(title="AgentLab API", version="1.0.0")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # For dev MVP
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(router, prefix="/api/v1")
    
    # Register tools
    registry.register(WikipediaTool())
    registry.register(TavilyTool())
    registry.register(AddTool())
    registry.register(MultiplyTool())
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
