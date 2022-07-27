
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    project_name: str = Field('Billing', env='PROJECT_NAME')

    db_driver: str = Field('postgresql', env='DRIVER')
    db_host: str = Field('localhost', env='DB_HOST')
    db_port: str = Field('5432', env='DB_PORT')
    db_name: str = Field('billing_db', env='POSTGRES_DB')
    db_user: str = Field('postgres', env='POSTGRES_USER')
    db_password: str = Field('11111111', env='POSTGRES_PASSWORD')

    auth_url: str = Field('auth_service', env='AUTH_URL')
    auth_sync_path: str = Field('/api/v1/sync', env='AUTH_SYNC_PATH')
    auth_token: str = Field('super-secret-token', env='AUTH_TOKEN')

    admin_url: str = Field('auth_service', env='ADMIN_URL')
    admin_sync_path: str = Field('/api/v1/sync', env='ADMIN_SYNC_PATH')
    admin_login: str = Field('user', env='ADMIN_LOGIN')
    admin_password: str = Field('pass', env='ADMIN_PASSWORD')

    yookassa_account_id: int = Field('924950', env='YOOKASSA_ACCOUNT_ID')
    yookassa_secret_key: str = Field('test_JAcHY0noVjN5FuiIXRGasyUm0PrRb1H04fwKTMz9tss', env='YOOKASSA_SECRET_KEY')

    class Config:
        env_file = ".env"
