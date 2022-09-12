#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


import click
import unittest

from flask_migrate import Migrate, upgrade
from server import create_app, db
from server.model.rbca import Role

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


# @app.before_request
# def before_request():
#     pass
#
#
# @app.after_request
# def after_request():
#     pass


@app.cli.command()
def deploy():
    """发布命令"""
    # 迁移数据库
    upgrade()
    # 创建角色
    Role.insert_roles()


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
