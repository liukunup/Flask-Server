#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime
from flask import url_for
from .. import db
from ..exceptions import InvalidException


class User(db.Model):
    # 表名称
    __tablename__ = "user"
    # 表字段
    # 记录编号
    id = db.Column(db.BigInteger, primary_key=True)
    # 业务字段
    nickname = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # 记录时间
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def to_json(self):
        json_obj = {
            "url": url_for("api.get_user", uid=self.id),
            "id": self.id,
            "nickname": self.nickname,
            "username": self.username,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }
        return json_obj

    @staticmethod
    def from_json(json_obj):
        nickname = json_obj.get("nickname")
        username = json_obj.get("username")
        if username is None or username == "" or len(username) > 64:
            raise InvalidException("提交信息中 username 参数不合法!", condition="最长64个字符的非空字符串.")
        return User(username=username, nickname=nickname)

    def __repr__(self):
        return "<User %r>" % self.username
