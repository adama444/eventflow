import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Define all project settings"""

    # App
    app_name: str = Field(default="EventFlow")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=True)

    # Google Drive
    google_drive_credentials: str = "credentials.json"
    drive_folder_id: str = Field(default="")
    drive_media_folder_id: str = Field(default="")
    google_oauth_token: str = "token.json"

    # LangSmith / LangChain
    langsmith_tracing: bool = Field(default=False)
    langsmith_endpoint: str | None = None
    langsmith_api_key: str | None = None
    langsmith_project: str | None = None

    # Groq API
    ollama_model: str = "llama3.2:3b"

    # Database
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db_name: str = "eventflow"

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db_name}"
        )

    @property
    def psycopg_database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db_name}"
        )

    def configure_langsmith(self):
        """Configure LangSmith environment variables if tracing is enabled."""
        if self.langsmith_tracing:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            if self.langsmith_endpoint:
                os.environ["LANGCHAIN_ENDPOINT"] = self.langsmith_endpoint
            if self.langsmith_api_key:
                os.environ["LANGCHAIN_API_KEY"] = self.langsmith_api_key
            if self.langsmith_project:
                os.environ["LANGCHAIN_PROJECT"] = self.langsmith_project


settings = Settings()
settings.configure_langsmith()
