import os
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(f"{Path(os.getcwd())}/src/config/.env")

db = SQLAlchemy()
migrate = Migrate()


def init_db(app: Flask):
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{os.getenv("POSTGRES_USER")}:' \
        f'{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("DB_HOST_AUTH")}/{os.getenv("DB_NAME_AUTH")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

@contextmanager
def session_db():
    engine = create_engine(f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
                           f"{os.getenv('DB_HOST_AUTH')}/{os.getenv('DB_NAME_AUTH')}")
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()



@contextmanager
def session_scope():
    try:
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
