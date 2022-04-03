#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

from flask_migrate import Migrate, upgrade
from server import create_app, db
from server.model.system import Role, App

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.cli.command()
def deploy():
    """发布命令"""
    # 迁移数据库
    upgrade()
    # 创建角色
    Role.insert_roles()
    # 创建超级管理员
    App.add_super_admin(os.getenv('SUPER_ADMIN'), 'This is a super administrator.', 'Admin')
