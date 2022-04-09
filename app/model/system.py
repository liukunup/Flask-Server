#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import string

from datetime import datetime
from flask import current_app, url_for
from .. import db
from ..exceptions import InvalidException


class Permission:
    """
    权限 读写改删 / 超级管理
    """
    READ = 1
    WRITE = 2
    UPDATE = 4
    DELETE = 8
    ADMIN = 16


class Role(db.Model):
    """
    角色
    """
    # 表名称
    __tablename__ = "role"
    # 表字段
    # 记录编号
    id = db.Column(db.Integer, primary_key=True)
    # 名称
    name = db.Column(db.String(16), comment="角色", unique=True)
    # 是否为默认角色
    default = db.Column(db.Boolean, comment="是否为默认角色", default=False, index=True)
    # 权限
    permissions = db.Column(db.Integer, comment="权限")
    # 应用 多对一
    apps = db.relationship("App", backref="role", lazy="dynamic")
    # 记录时间
    create_time = db.Column(db.DateTime(), comment="创建时间", default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), comment="更新时间", default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            "Follower": [Permission.READ],
            "Executor": [Permission.READ, Permission.WRITE],
            "Owner": [Permission.READ, Permission.WRITE, Permission.UPDATE, Permission.DELETE],
            "Administrator": [Permission.READ, Permission.WRITE, Permission.UPDATE, Permission.DELETE, Permission.ADMIN]
        }
        default_role = "Follower"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return "<Role %r>" % self.name


class App(db.Model):
    """
    应用
    """
    # 表名称
    __tablename__ = "app"
    # 表字段
    # 记录编号
    id = db.Column(db.Integer, primary_key=True)
    # 名称+描述
    name = db.Column(db.String(128), comment="名称", nullable=False, unique=True, index=True)
    desc = db.Column(db.String(256), comment="描述")
    # 角色
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    # 所有者
    owner = db.Column(db.String(64), comment="所有者(工号或昵称)", nullable=False, index=True)
    # AK+SK 密钥对
    access_key = db.Column(db.String(32), comment="公钥", nullable=False, unique=True, index=True)
    secret_key = db.Column(db.String(32), comment="私钥", nullable=False)
    # 是否已启用
    is_enabled = db.Column(db.Boolean, comment="是否已启用", default=False, index=True)
    # 记录时间
    create_time = db.Column(db.DateTime(), comment="创建时间", default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), comment="更新时间", default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def add_super_admin(name, desc, owner):
        # 检查是否已存在超级管理员
        for app in App.query.all():
            if app.name == name:
                print("The super administrator had been created.")
                return
        # 创建超级管理员
        app = App(name=name, desc=desc, owner=owner, is_enabled=True)
        db.session.add(app)
        db.session.commit()

    def __init__(self, **kwargs):
        super(App, self).__init__(**kwargs)
        if self.role is None:
            if self.name == current_app.config["SUPER_ADMIN"]:
                self.role = Role.query.filter_by(name="Administrator").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        # 自动生成32位AK+SK
        if self.access_key is None:
            self.access_key = "".join(random.sample(string.digits + string.ascii_letters, 32))
        if self.secret_key is None:
            self.secret_key = "".join(random.sample(string.digits + string.ascii_letters, 32))
        # 参数检查
        if self.name is None or self.name == "" or len(self.name) > 128:
            raise InvalidException("提交信息中 name 参数不合法!", condition="最长128字符的非空字符串.")
        if self.desc is not None and len(self.desc) > 256:
            raise InvalidException("提交信息中 desc 参数不合法!", condition="最长256字符,可空.")
        if self.owner is None or self.owner == "" or len(self.owner) > 64:
            raise InvalidException("提交信息中 owner 参数不合法!", condition="最长64字符的非空字符串.")

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def to_json(self):
        ret = {
            "url": url_for("api.get_app", app_id=self.id),
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "role_id": self.role_id,
            "owner": self.owner,
            "access_key": self.access_key,
            "is_enabled": self.is_enabled,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }
        return ret

    @staticmethod
    def from_json(obj):
        name = obj.get("name")
        desc = obj.get("desc")
        owner = obj.get("owner")
        return App(name=name, desc=desc, owner=owner)

    def __repr__(self):
        return "<App %r>" % self.name
