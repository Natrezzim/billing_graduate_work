import os
from functools import wraps

from app.data.datastore.token_datastore import TokenDataStore
from flask import request

SECRET_KEY = os.getenv('JWT_SECRET_KEY')


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            body = request.args
            access_data = TokenDataStore.get_user_data_from_token(token=body['access_token'], secret_key=SECRET_KEY)
            if access_data["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return {"message": "Admins only!"}, 403

        return decorator

    return wrapper
