#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import jsonify, request, url_for
from . import api
from .. import db
from ..model.user import User


@api.route('/users/<int:uid>', methods=["GET"])
def get_user(uid):
    user = User.query.get_or_404(uid)
    return jsonify(user.to_json())


@api.route('/users', methods=["POST"])
def add_user():
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 201, {'Location': url_for('api.get_user', uid=user.id)}
