#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import jsonify
from . import api
from ..model.system import App


@api.route('/apps/<int:app_id>', methods=["GET"])
def get_app(app_id):
    app = App.query.get_or_404(app_id)
    return jsonify(app.to_json())
