# -*- coding: UTF-8 -*-
# author:      Liu Kun
# email:       liukunup@outlook.com
# timestamp:   2022/9/11 16:44
# description: Open API (使用RBCA权限控制系统)

import random
import string

from datetime import datetime
from server import db
from server.bean.error import InvalidParamException


class Permission:
    """ 权限 """

    READ = 1
    WRITE = 2
    UPDATE = 4
    DELETE = 8
    ADMIN = 16


class Role(db.Model):
    """ 角色 """

    # 表名称
    __tablename__ = "role"

    # 记录编号
    id = db.Column(db.BigInteger, comment="记录编号", primary_key=True)
    # 业务字段
    name = db.Column(db.String(16), comment="角色名", unique=True)
    is_default = db.Column(db.Boolean, comment="是否默认角色", default=False)
    permissions = db.Column(db.Integer, comment="权限值")
    robots = db.relationship("MachineUser", backref="role", lazy="dynamic")
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


class MachineUser(db.Model):
    """ 机器用户 """

    # 表名称
    __tablename__ = "machine_user"

    # 记录编号
    id = db.Column(db.BigInteger, primary_key=True)
    # 业务字段
    name = db.Column(db.String(128), comment="名称", nullable=False, unique=True)
    desc = db.Column(db.String(256), comment="描述")
    owner = db.Column(db.String(64), comment="所有者(工号或昵称)", nullable=False)
    access_key = db.Column(db.String(32), comment="公钥", nullable=False, unique=True)
    secret_key = db.Column(db.String(32), comment="私钥", nullable=False)
    is_enabled = db.Column(db.Boolean, comment="是否已启用", nullable=False, default=True)
    role_id = db.Column(db.BigInteger, db.ForeignKey("role.id"))
    # 记录时间
    create_time = db.Column(db.DateTime(), comment="创建时间", default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), comment="更新时间", default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(MachineUser, self).__init__(**kwargs)
        # 参数检查
        if not self.name or len(self.name) > 128:
            raise InvalidParamException(error="提交信息中 name 参数不合法!", value=self.name,
                                        suggestions=["字段要求: 最长128字符的非空字符串"])
        if self.desc is not None and len(self.desc) > 256:
            raise InvalidParamException(error="提交信息中 desc 参数不合法!", value=self.desc,
                                        suggestions=["字段要求: 最长256字符的非空字符串, 可置空"])
        if not self.owner or len(self.owner) > 64:
            raise InvalidParamException(error="提交信息中 owner 参数不合法!", value=self.owner,
                                        suggestions=["字段要求: 最长64字符的非空字符串"])
        # 默认角色为Follower
        if not self.role:
            self.role = Role.query.filter_by(is_default=True).first()
        # 自动生成32位AK+SK
        if self.access_key is None:
            self.access_key = "".join(random.sample(string.digits + string.ascii_letters, 32))
        if self.secret_key is None:
            self.secret_key = "".join(random.sample(string.digits + string.ascii_letters, 32))

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    @staticmethod
    def from_json(obj):
        return MachineUser(name=obj.get("name"), desc=obj.get("desc"), owner=obj.get("owner"))

    def __repr__(self):
        return "<MachineUser %r>" % self.name
