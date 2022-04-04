from flask import Blueprint, jsonify
from ..exceptions import BaseCustomException

api = Blueprint("api", __name__)

from . import user, system


@api.errorhandler(BaseCustomException)
def invalid_value(e):
    return jsonify(e.to_dict())
