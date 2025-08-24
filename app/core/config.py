from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Define all project settings"""

    # App
    app_name: str = Field(default="EventFlow")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=True)

    # Google Drive
    google_drive_credentials: str
    drive_folder_id: str
    drive_media_folder_id: str

    # LangSmith / LangChain
    langsmith_tracing: bool = Field(default=False)
    langsmith_endpoint: str | None = None
    langsmith_api_key: str | None = None
    langsmith_project: str | None = None

    # Groq API
    groq_api_key: str
    groq_model: str

    # Database
    postgres_user: str
    postgres_password: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db_name: str

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        return (
            f"dbname={self.postgres_db_name} "
            f"user={self.postgres_user} "
            f"password={self.postgres_password} "
            f"host={self.postgres_host} "
            f"port={self.postgres_port}"
        )


settings = Settings()
