#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

from flask_migrate import Migrate, upgrade
from server import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.cli.command()
def create():
    """创建数据库"""
    if input("即将创建所有表,是否继续? [Yes/No] ") in ["Yes", "Y", "y"]:
        # 创建所有表
        db.create_all()
    pass


@app.cli.command()
def destroy():
    """销毁数据库"""
    if input("即将删除所有表以及数据,是否继续? [Yes/No] ") in ["Yes", "Y", "y"]:
        # 删除所有表以及数据
        db.drop_all()
    pass
