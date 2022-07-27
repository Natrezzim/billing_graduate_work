
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    project_name: str = Field('Billing', env='PROJECT_NAME')

    auth_secret: str = Field('verystrongsecretkey', env='AUTH_SECRET')

    db_driver: str = Field('postgresql', env='DRIVER')
    db_host: str = Field('postgres', env='DB_HOST_BILLING')
    db_port: str = Field('5432', env='DB_PORT_BILLING')
    db_name: str = Field('billing_db', env='DB_NAME_BILLING')
    db_user: str = Field('postgres', env='POSTGRES_USER')
    db_password: str = Field('1234', env='POSTGRES_PASSWORD')

    yookassa_account_id: int = Field('924950', env='YOOKASSA_ACCOUNT_ID')
    yookassa_secret_key: str = Field('test_JAcHY0noVjN5FuiIXRGasyUm0PrRb1H04fwKTMz9tss', env='YOOKASSA_SECRET_KEY')
    yookassa_access_token: str = Field('AAEACFY1AEGN1AAAAYIS464YODN6gzOk7JHDiA3qIZSMeafVj6SMd0aJsWU9auLuT7EI9PylypRgRYugMBJ618fD', env='YOOKASSA_ACCESS_TOKEN')

    class Config:
        env_file = ".env"
