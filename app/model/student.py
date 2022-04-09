from datetime import datetime
from flask import url_for
from .. import db
from ..exceptions import InvalidException


class Student(db.Model):
    # 表名称
    __tablename__ = "student"
    # 表字段
    # 记录编号
    id = db.Column(db.BigInteger, primary_key=True)
    # 业务字段
    name = db.Column(db.String(64), comment="姓名")
    sex = db.Column(db.Enum("Male", "Female", "Unknown"), comment="性别", default="Unknown", nullable=True)
    birthday = db.Column(db.DateTime(), comment="生日", default=None, nullable=True)
    # 记录时间
    create_time = db.Column(db.DateTime(), comment="创建时间", default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), comment="更新时间", default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Student, self).__init__(**kwargs)
        if self.name is None or self.name == "" or len(self.name) > 64:
            raise InvalidException("提交信息中 name 参数不合法!", condition="最长64个字符的非空字符串.")

    def to_json(self):
        ret = {
            "url": url_for("api.get_student", stu_id=self.id),
            "id": self.id,
            "name": self.name,
            "sex": self.sex,
            "birthday": self.birthday,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }
        return ret

    @staticmethod
    def from_json(obj):
        name = obj.get("name")
        sex = obj.get("sex")
        birthday = obj.get("birthday")
        return Student(name=name, sex=sex, birthday=birthday)

    def __repr__(self):
        return "<Student %r>" % self.name
