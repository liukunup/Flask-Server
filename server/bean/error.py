# -*- coding: UTF-8 -*-
# author:      Liu Kun
# email:       liukunup@outlook.com
# timestamp:   2022-09-10 23:01:00
# description: Error

__all__ = [
    "UnknownException",
    "InvalidParamException",
    "NoPermissionException",
    "DiffSignatureException",
]

from typing import Text, List, Any
from server.bean import Integer, Float
from server.bean.response import ApiResponse


class UnknownException(ApiResponse, Exception):
    """ 未定义异常 """

    # 不建议直接返回一个未定义的异常消息
    def __init__(self, code: Integer, message: Text, time_elapsed_ms: Float = None,
                 error: Text = None, value: Any = None, suggestions: List[Text] = None):
        # 当返回一个错误时，需要明确错误原因、当前错误值以及修复客户端建议
        payload = dict()
        if error:
            payload.update({"error": error})
        if value:
            payload.update({"value": value})
        if suggestions:
            payload.update({"suggestions": suggestions})
        # 调用父类封装
        super().__init__(code=code, message=message, payload=payload, time_elapsed_ms=time_elapsed_ms)


class InvalidParamException(UnknownException):
    """ 无效参数 """

    def __init__(self, error: Text = None, value: Any = None, suggestions: List[Text] = None):
        super().__init__(code=-1001, message="无效参数", error=error, value=value, suggestions=suggestions)


class NoPermissionException(UnknownException):
    """ 权限不足 """

    def __init__(self, error: Text = None, value: Any = None, suggestions: List[Text] = None):
        super().__init__(code=-2001, message="权限不足", error=error, value=value, suggestions=suggestions)


class DiffSignatureException(UnknownException):
    """ 签名不一致 """

    def __init__(self, error: Text = None, value: Any = None, suggestions: List[Text] = None):
        super().__init__(code=-2002, message="签名不一致", error=error, value=value, suggestions=suggestions)
