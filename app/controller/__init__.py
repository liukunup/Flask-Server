from flask import Blueprint, jsonify
from ..exceptions import BaseCustomException

api = Blueprint("api", __name__)

from . import system, student


@api.errorhandler(BaseCustomException)
def base_custom_exception(e):
    """捕获所有自定义的异常情况"""
    return jsonify(e.to_dict())
