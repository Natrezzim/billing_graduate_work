import os

from flask import Flask
from flask_xcaptcha import XCaptcha

xcaptcha = XCaptcha()


def init_captcha(app: Flask):
    """

    :param app:
    """
    app.config.update(
        XCAPTCHA_SITE_KEY=os.getenv("XCAPTCHA_SITE_KEY"),
        XCAPTCHA_SECRET_KEY=os.getenv("XCAPTCHA_SECRET_KEY")
    )
    xcaptcha.__init__(app=app)

