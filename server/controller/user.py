#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import jsonify, request, url_for
from . import api
from .. import db
from ..model.user import User
from ..results import Success, Failed


@api.route("/users/<int:uid>", methods=["GET"])
def get_user(uid):
    user = db.session.query(User).filter(User.id == uid).first()
    if user is None:
        return jsonify(Failed(None).to_dict())
    return jsonify(Success(user.to_json()).to_dict())


@api.route("/users", methods=["POST"])
def add_user():
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify(Success(user.to_json()).to_dict()), 201, {"Location": url_for("api.get_user", uid=user.id)}


@api.route("/users/<int:uid>", methods=["DELETE"])
def del_user(uid):
    db.session.query(User).filter(User.id == uid).delete()
    db.session.commit()
    return jsonify(Success(None).to_dict())
