import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    参数配置基类
    """
    # SUPER_ADMIN
    SUPER_ADMIN = os.environ.get("SUPER_ADMIN")
    # USE_TALISMAN
    USE_TALISMAN = False
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
    # 测试标识
    TESTING = True
    # 常用测试数据库（局域网专用实例）
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


class DockerConfig(ProductionConfig):
    """
    Docker 生产环境配置
    """
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
    """
    Unix 生产环境配置
    """
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
    # 默认使用开发环境
    "default": DevelopmentConfig
}
