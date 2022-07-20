import datetime
import http
import os

from app.data.db.redis import redis_conn
from flask import Flask, jsonify, request


def init_rate_limit(app: Flask):
    """

    :param app:
    :return:
    """
    @app.before_request
    def rate_limit(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        pipe = redis_conn.pipeline()
        now = datetime.datetime.now()
        key = f'{request.remote_addr}:{now.minute}'
        pipe.incr(key, 1)
        pipe.expire(key, 59)
        result = pipe.execute()
        request_number = result[0]
        if request_number > int(os.getenv("REQUEST_LIMIT_PER_MINUTE")):
            return jsonify(
                msg={
                    http.HTTPStatus.TOO_MANY_REQUESTS: "Too Many Requests"
                })
