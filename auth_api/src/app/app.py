import json
import logging
import os

from app.api.v1.routes.routes import initialize_routes
from app.api.v1.service.auth_service.auth_api import auth, auth_namespace
from app.api.v1.service.auth_service.billing_sync import billing_sync_namespace, sync
from app.api.v1.service.role_service.cli_commands import adm_cmd
from app.api.v1.service.role_service.roles_api import role_namespace, roles
from app.data.db.db import init_db
from app.miscellaneous.jaeger import init_jaeger
from app.miscellaneous.jaeger_config import configure_tracer
from app.miscellaneous.rate_limit import init_rate_limit
from app.miscellaneous.xcaptcha_config import init_captcha
from app.oauth.oauth import init_oauth
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_qrcode import QRcode
from flask_restx import Api
from opentelemetry.instrumentation.flask import FlaskInstrumentor

load_dotenv(f'{os.getcwd()}/.env')

app = Flask(__name__)

log_format = {"asctime": "%(asctime)s","levelname": "%(levelname)s","name": "%(name)s","threadName": "%(threadName)s","message": "%(message)s"}
logging.basicConfig(filename='/usr/src/app/logs/auth_logs.log',
                    level=logging.DEBUG,
                    format=json.dumps(log_format))

jwt = JWTManager(app)

api = Api(app, version='1.0', title='Auth API',
          description='Сервис авторизации', doc='/docs/')

app.config["SECRET_KEY"] = '3212gregbergqfwwe'

app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
QRcode(app)
init_db(app)
init_oauth(app)
initialize_routes(api)
app.register_blueprint(auth)
app.register_blueprint(roles)
app.register_blueprint(adm_cmd)
app.register_blueprint(sync)
api.add_namespace(role_namespace)
api.add_namespace(auth_namespace)
api.add_namespace(billing_sync_namespace)
init_rate_limit(app)
init_jaeger(app)
configure_tracer()
FlaskInstrumentor().instrument_app(app)
init_captcha(app)

if __name__ == '__main__':
    app.run()
