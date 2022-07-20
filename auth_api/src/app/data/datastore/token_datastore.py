import datetime
import uuid
from typing import Optional

import jwt
from app.data.db.db import db, session_scope
from app.data.db.db_models import Tokens
from sqlalchemy import delete, update


class TokenDataStore:

    @staticmethod
    def create_jwt_token(user_id: uuid.UUID, username: str, password: str, secret_key: str,
                         expires_delta: datetime.timedelta,  admin: Optional[bool] = None) -> str:
        """
        Создание jwt token

        :param admin:
        :param user_id:
        :param username: имя пользователя
        :param password: пароль
        :param secret_key: подпись токена
        :param expires_delta: время действия токена
        :return:
        """
        current_time = datetime.datetime.now()
        expiries_time = current_time + expires_delta
        payload = {
            "user_id": str(user_id),
            "username": str(username),
            "password": str(password),
            "expires": str(expiries_time.strftime("%Y-%m-%dT%H:%M:%S")),
            "type": "access",
            "is_administrator": admin
        }
        token = jwt.encode(
            payload=payload,
            key=str(secret_key)
        )
        return token

    @staticmethod
    def create_refresh_token(username: str, password: str, secret_key: str, expires_delta: datetime.timedelta,
                             user_id, admin: Optional[bool] = None) -> str:
        """
        Создание refresh token

        :param admin:
        :param user_id:
        :param username: имя пользователя
        :param password: пароль
        :param secret_key: подпись токена
        :param expires_delta: время действия токена
        :return:
        """
        current_time = datetime.datetime.now()
        expiries_time = current_time + expires_delta
        payload = {
            "user_id": str(user_id),
            "username": str(username),
            "password": str(password),
            "expires": str(expiries_time.strftime("%Y-%m-%dT%H:%M:%S")),
            "type": "refresh",
            "is_administrator": admin
        }
        token = jwt.encode(
            payload=payload,
            key=str(secret_key)
        )
        return token

    @staticmethod
    def get_user_data_from_token(token: str, secret_key: str):
        """
        Получаем информацию о пользователе из jwt токена

        :param token:
        :param secret_key:
        :return:
        """
        data = jwt.decode(jwt=token, key=secret_key, algorithms="HS256")
        return data

    @staticmethod
    def save_refresh_token(refresh_token: str, user_id):
        """
        Сохраняет refresh token в БД
        :param refresh_token:
        :param user_id:
        :return:
        """
        current_refresh = Tokens.query.filter_by(user_id=user_id).one_or_none()
        if current_refresh is None:
            data = Tokens(id=uuid.uuid4(), user_id=user_id, refresh_token=refresh_token)
            with session_scope():
                db.session.add(data)
                db.session.commit()

        else:
            stmt = update(Tokens).where(Tokens.user_id == user_id).values(refresh_token=refresh_token). \
                execution_options(synchronize_session="fetch")
            with session_scope():
                db.session.execute(stmt)
                db.session.commit()

    @staticmethod
    def get_refresh_token(user_id):
        token_info = Tokens.query.filter_by(user_id=user_id).one_or_none()
        if token_info is not None:
            return token_info.refresh_token

    @staticmethod
    def delete_refresh_token(refresh_token: str):
        """
        Удаляет refresh token в БД
        :param refresh_token:
        :return:
        """
        with session_scope():
            stmt = delete(Tokens).where(Tokens.refresh_token == refresh_token)
            db.session.execute(stmt)
            db.session.commit()
