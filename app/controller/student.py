from flask import jsonify, request, url_for
from . import api
from .. import db
from ..model.student import Student
from ..results import Success, Failed


@api.route("/students/<int:stu_id>", methods=["GET"])
def get_student(stu_id):
    student = db.session.query(Student).filter(Student.id == stu_id).first()
    if student is None:
        return jsonify(Failed("No such student.").to_dict())
    return jsonify(Success(student.to_json()).to_dict())


@api.route("/students", methods=["POST"])
def add_student():
    student = Student.from_json(request.json)
    db.session.add(student)
    db.session.commit()
    return jsonify(Success(student.to_json()).to_dict()), 201, {"Location": url_for("api.get_student", stu_id=student.id)}


@api.route("/students/<int:stu_id>", methods=["DELETE"])
def del_student(stu_id):
    db.session.query(Student).filter(Student.id == stu_id).delete()
    db.session.commit()
    return jsonify(Success(None).to_dict())


@api.route("/students/<int:stu_id>", methods=["PUT"])
def upd_student(stu_id):
    kv_dict = dict()  # 存储待更新的KV
    # 哪些字段可被更新
    supported_keys = ["name", "sex", "birthday"]
    # 获取新值
    obj = request.json
    for key in supported_keys:
        if key in obj:
            kv_dict.update({key: obj[key]})
    # 更新
    db.session.query(Student).filter(Student.id == stu_id).update(kv_dict)
    db.session.commit()
    # 查询
    student = db.session.query(Student).filter(Student.id == stu_id).first()
    if student is None:
        return jsonify(Failed("No such student.").to_dict())
    # 返回结果
    return jsonify(Success(student.to_json()).to_dict()), 201, {"Location": url_for("api.get_student", stu_id=stu_id)}
