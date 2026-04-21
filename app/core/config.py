from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Auron API"
    app_env: str = "local"
    api_v1_prefix: str = "/api/v1"

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    api_url: str
    media_url: str
    storage_path: str

    postgres_db: str = "auron"
    postgres_user: str = "auron_user"
    postgres_password: str = "auron_pass"
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
