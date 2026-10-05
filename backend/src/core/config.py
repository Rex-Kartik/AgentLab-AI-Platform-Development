from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str = "placeholder_for_groq_api_key"
    TAVILY_API_KEY: str = "placeholder_for_tavily_api_key"
    
    class Config:
        env_file = ".env"

settings = Settings()
