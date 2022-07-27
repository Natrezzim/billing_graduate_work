from app.data.datastore.user_datastore import UserDataStore
from app.oauth.oauth import oauth
from flask import Blueprint, redirect, url_for
from flask_restx import Resource

auth = Blueprint('oauth', __name__)


class LoginYandex(Resource):
    @staticmethod
    def get():
        """

        :return: redirect to AuthorizationYandex class
        """
        redirect_url = url_for("authorization_yandex", _external=True)
        return oauth.yandex.authorize_redirect(redirect_url)


class AuthorizationYandex(Resource):
    @staticmethod
    def get():
        """

        :return: redirect to
        """
        token = oauth.yandex.authorize_access_token()
        response = oauth.yandex.get('https://login.yandex.ru/info')
        response.raise_for_status()
        profile = response.json()
        user = UserDataStore.find_user_social_acc(social_id=profile['id'], social_name='yandex',
                                                  username=profile['login'])
        if not user:
            UserDataStore.register_user_with_social(username=profile['login'], email=profile['default_email'],
                                                    social_name='yandex', social_id=profile['id'])
            return redirect('/')
        else:
            return {"Message:": "User already exist"}
