# -*- coding: UTF-8 -*-
# author:      Liu Kun
# email:       liukunup@outlook.com
# timestamp:   2022-09-11 10:53:00
# description: Controller

from flask import Blueprint, jsonify
from server.bean.error import UnknownException

api = Blueprint("api", __name__)

from server.controller import healthz


@api.errorhandler(UnknownException)
def base_custom_exception(e):
    """捕获所有自定义的异常情况"""
    return jsonify(e.data())
