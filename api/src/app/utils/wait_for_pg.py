import logging
import os
from pathlib import Path

import backoff
import psycopg2
from dotenv import load_dotenv

load_dotenv(f"{Path(os.getcwd())}/config/.env")

logging.getLogger('backoff').addHandler(logging.StreamHandler())

dsl = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}


@backoff.on_exception(wait_gen=backoff.expo,
                      exception=(psycopg2.Error, psycopg2.OperationalError))
def postgres_conn():
    psycopg2.connect(**dsl)


if __name__ == '__main__':
    postgres_conn()
