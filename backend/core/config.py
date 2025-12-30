from pydantic import BaseModel
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"  #加密算法
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h  

    #page display: number of return rows in each page
    DEFAULT_LIMIT: int = 50
    MAX_LIMIT: int = 200
    DEFAULT_OFFSET: int = 0

    model_config = SettingsConfigDict(env_file = ".env", env_file_encoding= "utf-8")

settings = Settings()