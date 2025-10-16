from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str

    @property
    def database_url(self) -> str:
        return (f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}")
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
