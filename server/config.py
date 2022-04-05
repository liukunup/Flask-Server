#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    参数配置基类
    """
    # SECRET_KEY
    import random
    import string
    SECRET_KEY = os.environ.get("SECRET_KEY") or "".join(random.sample(string.digits + string.ascii_letters, 16))
    # SUPER_ADMIN
    SUPER_ADMIN = os.environ.get("SUPER_ADMIN")
    # SSL_REDIRECT
    SSL_REDIRECT = False
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    # PAGE
    ITEMS_PER_PAGE = 25

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    开发环境配置
    """
    # 日志等级设置到DEBUG
    DEBUG = True
    # 回显SQL语句
    SQLALCHEMY_ECHO = True
    # 数据库链接
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "dev.sqlite")


class TestingConfig(Config):
    """
    测试环境配置
    """
    #
    TESTING = True
    #
    MYSQL_HOST = os.environ.get("MYSQL_HOST") or "127.0.0.1"
    MYSQL_PORT = os.environ.get("MYSQL_PORT") or "3306"
    MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME") or "root"
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or "123456"
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE") or "db"
    # 数据库链接
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/" \
                              f"{MYSQL_DATABASE}"


class ProductionConfig(Config):
    """
    生产环境配置
    """
    # 数据库链接
    MYSQL_HOST = os.environ.get("MYSQL_HOST") or "127.0.0.1"
    MYSQL_PORT = os.environ.get("MYSQL_PORT") or "3306"
    MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME") or "root"
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or "123456"
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE") or "db"
    # 数据库链接
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/" \
                              f"{MYSQL_DATABASE}"


config = {
    # 环境配置标识
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
    "default": DevelopmentConfig
}
