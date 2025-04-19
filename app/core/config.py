import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

class Settings(BaseSettings):
    """Configurações da aplicação lidas do ambiente/arquivo .env."""
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS_STR: str = "http://localhost:3000,http://127.0.0.1:3000"
    MARIADB_ROOT_PASSWORD: str
    MARIADB_DATABASE: str
    MARIADB_USER: str
    MARIADB_PASSWORD: str

    # Propriedade calculada para ter a lista
    @property
    def CORS_ORIGINS(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS_STR.split(",")]

    class Config:
        # Define o arquivo .env a ser lido
        env_file = ".env"
        case_sensitive = False

settings = Settings()
