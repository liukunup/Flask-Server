# -*- coding: UTF-8 -*-
# author:      Liu Kun
# email:       liukunup@outlook.com
# timestamp:   2022/9/11 13:39
# description: Configuration

import os

from urllib.parse import quote
from flask_limiter.util import get_remote_address


class Config:
    """ 配置基类 """

    # SUPER_ADMIN
    SUPER_ADMIN = os.environ.get("SUPER_ADMIN")

    # MYSQL
    MYSQL_HOST = os.environ.get("MYSQL_HOST") or "127.0.0.1"
    MYSQL_PORT = os.environ.get("MYSQL_PORT") or "3306"
    MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME") or "root"
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or "123456"
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE") or "db"
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{quote(MYSQL_USERNAME)}:{quote(MYSQL_PASSWORD)}" \
                              f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # Limiter
    RATELIMIT_DEFAULT = "10 per day;3 per hour"
    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_HEADERS_ENABLED = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """ 开发环境 """
    # 日志等级设置到DEBUG
    DEBUG = True
    # 回显SQL语句
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """ 测试环境 """
    # 测试标识
    TESTING = True


class ProductionConfig(Config):
    """ 生产环境 """


class DockerConfig(ProductionConfig):
    """ Docker """
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        # log to stderr
        import logging
        from logging import StreamHandler
        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)


class UnixConfig(ProductionConfig):
    """ Unix """
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.INFO)
        app.logger.addHandler(syslog_handler)


config = {
    # 环境标识
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "docker": DockerConfig,
    "unix": UnixConfig,
    # 默认环境
    "default": DevelopmentConfig
}
