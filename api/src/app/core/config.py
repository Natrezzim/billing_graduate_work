
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    project_name: str = Field('Billing', env='PROJECT_NAME')

    db_host: str = Field('postgres', env='DB_HOST')
    db_user: str = Field('postgres', env='POSTGRES_USER')
    db_password: str = Field('1234', env='POSTGRES_PASSWORD')

    class Config:
        env_file = ".env"
