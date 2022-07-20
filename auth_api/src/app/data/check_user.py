import datetime
import os

from app.data.datastore.token_datastore import TokenDataStore
from app.data.db.db_models import Users


class CheckAuthUser:

    def __init__(self, secret_key=None):
        self.secret_key = os.getenv('JWT_SECRET_KEY') if secret_key is None else secret_key

    def check_access_token(self, token: str, service: str = "flask"):
        """
        Проверка валидности токена
        :param token: Токен
        :return:
        """
        # Получаем данные пользователя
        token_data = TokenDataStore.get_user_data_from_token(token=token, secret_key=self.secret_key)
        # Проверяем наличие пользователя в БД
        check_user = Users.query.filter_by(id=token_data['user_id']).one_or_none()
        if check_user is None:
            return False
        # Проверяем срок действия токена
        current_time = datetime.datetime.now()
        expire_time_t = datetime.datetime.strptime(token_data["expires"], "%Y-%m-%dT%H:%M:%S")
        if current_time > expire_time_t:
            return False
        return True
