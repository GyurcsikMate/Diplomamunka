from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    sqlalchemy_string: str = "postgresql://user:passwordp@host/db"
    
settings = Settings()