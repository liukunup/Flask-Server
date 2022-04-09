#!/usr/bin/python
# -*- coding: UTF-8 -*-


class ApiResult:
    """
    返回对象
    """
    def __init__(self, message, code, payload=None):
        self.message = message
        self.code = code
        self.payload = payload

    def to_dict(self):
        ret = dict()
        ret["code"] = self.code
        ret["message"] = self.message
        if self.payload is not None:
            ret["data"] = self.payload
        return ret


class Success(ApiResult):
    """
    成功
    """
    def __init__(self, payload):
        super().__init__("success", 200, payload=payload)


class Failed(ApiResult):
    """
    失败
    """
    def __init__(self, payload):
        super().__init__("failed", -1, payload=payload)
