from http import HTTPStatus
from typing import Dict

import jwt
from app.core.config import Settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

settings = Settings()


class Auth:
    secret = settings.auth_secret

    def decode_token(self, token: str) -> Dict[str, int]:
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if payload['type'] == 'access':
                return payload['user_id']
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid token')

    def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> Dict[str, int]:
        token = credentials.credentials
        return self.decode_token(token)
