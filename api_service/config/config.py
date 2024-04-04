from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    PROJECT_NAME: str
    STOCK_API_URL: str

    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"


settings = Settings()
