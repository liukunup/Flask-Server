import os
import unittest

from app import create_app, db
from app.model.system import Role, App


class BaseTest(unittest.TestCase):
    """
    测试基类
    """

    # 超级管理员密钥对
    access_key = "暂未配置"
    secret_key = "暂未配置"

    def setUp(self):
        # 创建应用（默认使用测试环境配置）
        self.app = create_app(os.getenv("FLASK_CONFIG") or "testing")
        # 获取上下文 并压入配置
        self.app_context = self.app.app_context()
        self.app_context.push()
        # 获取客户端实例
        self.client = self.app.test_client()
        # 创建数据表
        db.create_all()
        # 创建默认角色
        Role.insert_roles()
        # 创建超级管理员
        App.add_super_admin(os.getenv("SUPER_ADMIN"), "This is a super administrator.", "Admin")
        # 获取超级管理员
        self.getSuperAdmin()

    def tearDown(self):
        # 移除数据库会话
        db.session.remove()
        # 删除数据表
        db.drop_all()
        # 弹出上下文
        self.app_context.pop()

    def getSuperAdmin(self):
        """查询超级管理员"""
        app = db.session.query(App).filter(App.id == 1).first()
        self.assertIsNotNone(app)
        self.assertEqual(app.role.name, "Administrator")
        self.access_key = app.access_key
        self.secret_key = app.secret_key

    def expectRet(self, obj):
        self.assertIsNotNone(obj, "预期响应体不为None.")
        self.assertIn("code", obj, "预期包含字段code.")
        self.assertIn("message", obj, "预期包含字段message.")

    def expectSuccess(self, obj):
        self.expectRet(obj)
        self.assertEqual(obj["code"], 200, f"预期字段code值为200. message={obj['message']}")

    def expectFail(self, obj):
        self.expectRet(obj)
        self.assertEqual(obj["code"], -1, f"预期字段code值为-1. message={obj['message']}")
