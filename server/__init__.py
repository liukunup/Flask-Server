# -*- coding: UTF-8 -*-
# author:      Liu Kun
# email:       liukunup@outlook.com
# timestamp:   2022-09-11 13:27:00
# description: Application

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_cors import CORS
from server.configs import config

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
login_manager = LoginManager()
talisman = Talisman()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)
    talisman.init_app(app)
    CORS(app)

    from .controller import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
