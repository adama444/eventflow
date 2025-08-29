from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Define all project settings"""

    # App
    app_name: str = Field(default="EventFlow")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=True)

    # Google Drive
    google_drive_credentials: str = 'service_account.json'
    drive_folder_id: str = Field(default='')
    drive_media_folder_id: str = Field(default='')

    # LangSmith / LangChain
    langsmith_tracing: bool = Field(default=False)
    langsmith_endpoint: str | None = None
    langsmith_api_key: str | None = None
    langsmith_project: str | None = None

    # Groq API
    ollama_model: str = 'gemma3:1b'

    # Database
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db_name: str = 'eventflow'

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

settings = Settings()
