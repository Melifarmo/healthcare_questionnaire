from pydantic.v1 import BaseSettings


class AppSettings(BaseSettings):
    POSTGRES_DSN: str

    class Config:
        env_file = ".env"


settings = AppSettings()
