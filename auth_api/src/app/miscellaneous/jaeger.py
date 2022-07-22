from flask import Flask, request
from opentelemetry import trace


def init_jaeger(app: Flask):
    """

    :param app:
    """

    @app.before_request
    def before_request():
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            raise RuntimeError('request id is required')

    @app.before_request
    def request_id_tag():
        request_id = request.headers.get('X-Request-Id')
        tracer = trace.get_tracer("auth_service")
        span = tracer.start_span('request_id')
        span.set_attribute('http.request_id', request_id)
        span.end()
