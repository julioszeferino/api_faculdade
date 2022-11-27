from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseSettings

class Settings(BaseSettings):

    API_V1_STR: str = '/api/v1'
    BD_URL: str = "postgresql+asyncpg://admin:adminsenha@pgdb:5432/faculdade"
    DB_BASE_MODEL = declarative_base() 

    JWT_SECRET: str = 'yHXKahDXmk4USjRNW6IAIz56R5pufmMYDMqiqGeMXu' 
    ALGORITHM: str = 'HS256' 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 dias


    class config:
        case_sensitive = True

settings = Settings()