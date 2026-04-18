from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     app_name: str = "DeckPilot API"
#     app_version: str = "0.1.0"
#     debug: bool = True

#     database_url: str = ""
#     groq_api_key: str = ""
#     llm_model: str = "llama-3.3-70b-versatile"

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         case_sensitive=False,
#     )


class Settings(BaseSettings):
    app_name: str = "DeckPilot API"
    app_version: str = "0.1.0"
    debug: bool = True

    database_url: str = ""

    groq_api_key: str = ""
    llm1_model: str = "llama-3.3-70b-versatile"

    groq2_api_key: str = ""
    llm2_model: str = "llama-3.3-70b-versatile"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()

if not settings.database_url:
    raise ValueError("DATABASE_URL is not configured.")
