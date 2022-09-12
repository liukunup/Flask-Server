# -*- coding: UTF-8 -*-
# author:      Liu Kun
# email:       liukunup@outlook.com
# timestamp:   2022/9/11 00:17
# description: 健康检查

from flask import jsonify
from server.controller import api
from server.bean.response import Success


@api.route("/healthz/readness", methods=["GET", "POST"])
def readness():
    """ 就绪探针 """
    # (可选) 填充您的就绪逻辑
    return jsonify(Success().data())


@api.route("/healthz/liveness", methods=["GET", "POST"])
def liveness():
    """ 存活探针 """
    # (可选) 填充您的探活逻辑
    return jsonify(Success().data())
