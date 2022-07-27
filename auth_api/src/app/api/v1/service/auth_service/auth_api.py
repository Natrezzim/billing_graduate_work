import datetime
import os
from http import HTTPStatus

import pyotp
from app.data.check_user import CheckAuthUser
from app.data.datastore.roles_datastore import RolesCRUD
from app.data.datastore.token_datastore import TokenDataStore
from app.data.datastore.user_datastore import UserDataStore
from app.data.db.db_models import Tokens, Users
from app.miscellaneous.xcaptcha_config import xcaptcha
from app.utils.pagination import get_paginated_list
from flask import Blueprint, jsonify, make_response, redirect, render_template, request
from flask_restx import Namespace, Resource, fields, reqparse

auth = Blueprint('auth', __name__)

EXPIRE_REFRESH = datetime.timedelta(days=int(os.getenv('REFRESH_TOKEN_EXPIRED')))
EXPIRE_ACCESS = datetime.timedelta(hours=int(os.getenv('ACCESS_TOKEN_EXPIRED')))
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
AUTH_HISTORY_START_PAGE = os.getenv('AUTH_HISTORY_START_PAGE')
AUTH_HISTORY__PAGE_LIMIT = os.getenv('AUTH_HISTORY__PAGE_LIMIT')

auth_namespace = Namespace("auth", description='auth')

registration_model = auth_namespace.model('Registration', {
    'username': fields.String,
    'password': fields.String,
    'email': fields.String,
})


class RegistrationAPI(Resource):
    """
    логика работы метода для регистрации нового пользователя api/auth/registration
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="username")
    parser.add_argument('email', type=str, required=False, help="email")
    parser.add_argument('password', type=str, required=True, help="password")

    @staticmethod
    @auth_namespace.expect(registration_model)
    def post():
        body = request.get_json()
        # проверяем, что такого пользователя нет в БД
        check_user = Users.query.filter_by(username=body['username']).one_or_none()
        if check_user is not None:
            return {"error": {
                "message": "User with this username already exists"
            }}, HTTPStatus.CONFLICT
        else:
            UserDataStore.register_user(username=body["username"], password=body["password"], email=body["email"])
            return {"message": "Create new user success"}, HTTPStatus.OK


login_model = auth_namespace.model('Login', {
    'username': fields.String,
    'password': fields.String
})


class LoginApi(Resource):
    """
    логика работы метода api/auth/login
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="username")
    parser.add_argument('password', type=str, required=True, help="password")

    @staticmethod
    @auth_namespace.expect(login_model)
    def post():
        body = request.get_json()
        # проверяем авторизационные данные
        user_id = UserDataStore.authorize_user(username=body.get('username'), password=body.get('password'),
                                               user_agent=request.headers.get('User-Agent'))
        if user_id is None:
            return {"error": {
                "message": "Username or password invalid"}}, HTTPStatus.UNAUTHORIZED
        # генерируем access и refresh токены
        superuser = False
        for role in RolesCRUD.check_user_role(user_id):
            if role.role_type == 'superuser':
                superuser = True

        access_token = TokenDataStore.create_jwt_token(
            username=body["username"], password=body["password"], user_id=user_id, expires_delta=EXPIRE_ACCESS,
            secret_key=SECRET_KEY, admin=superuser)
        refresh_token = TokenDataStore.create_refresh_token(
            username=body["username"], password=body["password"], user_id=user_id, expires_delta=EXPIRE_REFRESH,
            secret_key=SECRET_KEY, admin=superuser)
        # Проверяем наличие refresh токена в БД
        current_refresh = TokenDataStore.get_refresh_token(user_id=user_id)
        if not current_refresh:
            # заливаем refresh токен в БД
            TokenDataStore.save_refresh_token(refresh_token=refresh_token, user_id=user_id)
        return {"access_token": access_token, "refresh_token": refresh_token, "message": "Login success"}, HTTPStatus.OK


refresh_model = auth_namespace.model('Refresh', {
    'access_token': fields.String,
    'refresh_token': fields.String
})


class RefreshAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('access_token', type=str, required=True, help="access_token")
    parser.add_argument('refresh_token', type=str, required=True, help="refresh_token")

    @staticmethod
    @auth_namespace.expect(refresh_model)
    def post():
        body = request.get_json()
        # Проверка Наличия refresh токена в БД
        refresh = Tokens.query.filter_by(refresh_token=body['refresh_token']).one_or_none()
        if refresh is None:
            return {"error": {"message": "Refresh token not valid"}}, HTTPStatus.UNAUTHORIZED
        # Проверка refresh tokena
        check_refresh_token = CheckAuthUser().check_access_token(token=body['refresh_token'])
        if check_refresh_token:
            # Проверяем access токен
            check_access_token = CheckAuthUser().check_access_token(token=body['refresh_token'])
            if check_access_token:
                return {"access_token": body['access_token'], "refresh_token": body['refresh_token']}
            else:
                # генерация новго access токена
                user_data = TokenDataStore.get_user_data_from_token(token=body['refresh_token'], secret_key=SECRET_KEY)
                new_access_token = TokenDataStore.create_jwt_token(
                    username=user_data["username"], password=user_data["password"], user_id=user_data["user_id"],
                    expires_delta=EXPIRE_ACCESS, secret_key=SECRET_KEY)
                return {"access_token": new_access_token, "refresh_token": body['refresh_token']}, HTTPStatus.OK


logout_model = auth_namespace.model('Logout', {
    'refresh_token': fields.String
})


class LogoutAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('refresh_token', type=str, required=True, help="refresh_token")

    @staticmethod
    @auth_namespace.expect(logout_model)
    def post():
        body = request.get_json()
        refresh = Tokens.query.filter_by(refresh_token=body['refresh_token']).one_or_none()
        if refresh is None:
            return {"error": {"message": "Refresh token not valid"}}, HTTPStatus.UNAUTHORIZED
        TokenDataStore.delete_refresh_token(refresh.refresh_token)
        return HTTPStatus.NO_CONTENT


hystory_model = auth_namespace.model('HistoryAuth', {
    'refresh_token': fields.String
})


class HistoryAuthAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('access_token', type=str, required=True, help="access_token")

    @staticmethod
    @auth_namespace.expect(hystory_model)
    def get():
        body = request.get_json()
        check_access_token = CheckAuthUser().check_access_token(token=body['access_token'])
        if check_access_token:
            access_data = TokenDataStore.get_user_data_from_token(token=body['access_token'], secret_key=SECRET_KEY)
            return jsonify({"history": get_paginated_list(
                UserDataStore.get_user_history_auth(user_id=access_data['user_id']), '/api/v1/auth_history',
                start=request.args.get('start', AUTH_HISTORY_START_PAGE),
                limit=request.args.get('limit', AUTH_HISTORY__PAGE_LIMIT))})
        return {"error": {"message": "Authorization token not valid"}}, HTTPStatus.UNAUTHORIZED


change_model = auth_namespace.model('ChangeAuthData', {
    'new_username': fields.String,
    'new_password': fields.String,
    'access_token': fields.String,
})


class ChangeAuthDataAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('new_username', type=str, help="login")
    parser.add_argument('new_password', type=str, help="password")
    parser.add_argument('access_token', type=str, required=True, help="access_token")

    @staticmethod
    @auth_namespace.expect(change_model)
    def post():
        body = request.get_json()
        check_access_token = CheckAuthUser().check_access_token(token=body['access_token'])
        if check_access_token:
            access_data = TokenDataStore.get_user_data_from_token(token=body['access_token'], secret_key=SECRET_KEY)
            UserDataStore.change_user(user_id=access_data["user_id"], new_username=body["new_username"],
                                      new_password=body["new_password"])


@auth_namespace.doc(params={'user_id': 'user_id'})
class Totp2FA(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, help="user_id")

    secret = pyotp.random_base32()

    def get(self):
        headers = {'Content-Type': 'text/html'}
        body = request.args
        totp = pyotp.TOTP(self.secret)
        user_info = UserDataStore.get_user_info(user_id=body['user_id'])
        provisioning_url = totp.provisioning_uri(name=user_info.username, issuer_name='Online Movies')
        if UserDataStore.check_user_totp(user_id=body['user_id']):
            return redirect(f"/api/v1/login/totp/login?user_id={body['user_id']}")

        return make_response(render_template('sync.html', url=provisioning_url, user_id=body['user_id']), 200,
                                 headers)

    def post(self):
        headers = {'Content-Type': 'text/html'}
        body = request.args
        if xcaptcha.verify():
            UserDataStore.add_totp_user(user_id=body['user_id'], secret=self.secret, verified=False)
        else:
            return make_response(render_template('robot.html'), 404, headers)
        secret = UserDataStore.check_user_totp(user_id=body['user_id']).secret
        totp = pyotp.TOTP(secret)
        code = request.form.get('code')
        if not totp.verify(code):
            return {'message': "wrong code"}
        else:
            UserDataStore.set_totp_verifiy(user_id=body['user_id'])
            return redirect(f"/api/v1/login/totp/login?user_id={body['user_id']}")


@auth_namespace.doc(params={'user_id': 'user_id'})
class Totp2FALogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, help="user_id")

    @staticmethod
    def get():
        headers = {'Content-Type': 'text/html'}
        body = request.args
        if not UserDataStore.check_user_totp(user_id=body['user_id']).verified:
            redirect('/')
        return make_response(render_template('check.html', message='', user_id=body['user_id']), 200, headers)

    @staticmethod
    def post():
        body = request.args
        headers = {'Content-Type': 'text/html'}
        if not UserDataStore.check_user_totp(user_id=body['user_id']).verified:
            redirect('/')

        code = request.form.get('code')
        secret = UserDataStore.check_user_totp(user_id=body['user_id']).secret
        totp = pyotp.TOTP(secret)

        if not totp.verify(code):
            return make_response(render_template('check.html', message='wrong code', user_id=body['user_id']), 200, headers)

        return redirect('/')
