
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    project_name: str = Field('Billing', env='PROJECT_NAME')

    db_host: str = Field('postgres', env='DB_HOST')
    db_port: str = Field('5432', env='DB_PORT')
    db_name: str = Field('billing_db', env='POSTGRES_DB')
    db_user: str = Field('postgres', env='POSTGRES_USER')
    db_password: str = Field('1234', env='POSTGRES_PASSWORD')

    yookassa_account_id: int = Field('924950', env='YOOKASSA_ACCOUNT_ID')
    yookassa_secret_key: str = Field('test_JAcHY0noVjN5FuiIXRGasyUm0PrRb1H04fwKTMz9tss', env='YOOKASSA_SECRET_KEY')

    class Config:
        env_file = ".env"
