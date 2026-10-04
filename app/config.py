from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
 database_url:str="postgresql+asyncpg://postgres:postgres@localhost:5432/router";api_key:str="change-me";max_candidates:int=20;mcp_mode:str="mock";rest_mode:str="mock";a2a_mode:str="mock"
 model_config=SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()
