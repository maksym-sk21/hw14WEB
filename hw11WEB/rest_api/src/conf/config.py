from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    postgres_db: str = os.getenv("POSTGRES_DB")
    postgres_user: str = os.getenv("POSTGRES_USER")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", 5432))

    sqlalchemy_database_url: str = os.getenv("SQLALCHEMY_DATABASE_URL")

    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")

    mail_username: str = os.getenv("MAIL_USERNAME")
    mail_password: str = os.getenv("MAIL_PASSWORD")
    mail_from: str = os.getenv("MAIL_FROM")
    mail_port: int = int(os.getenv("MAIL_PORT", 465))
    mail_server: str = os.getenv("MAIL_SERVER")

    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))


settings = Settings()
