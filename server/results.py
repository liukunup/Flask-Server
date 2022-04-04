#!/usr/bin/python
# -*- coding: UTF-8 -*-


class ApiResult:
    """
    返回对象
    """
    def __init__(self, code, message, payload=None):
        self.code = code
        self.message = message
        self.payload = payload

    def to_dict(self):
        ret = dict()
        ret["code"] = self.code
        ret["message"] = self.message
        if not self.payload:
            ret["data"] = self.payload
        return ret


class Success(ApiResult):
    """
    成功
    """
    def __init__(self, payload):
        super().__init__(200, "success", payload=payload)
