#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .results import ApiResult


class BaseCustomException(ApiResult, Exception):
    """
    自定义异常基类
    Tips: 异常返回也是接口返回的一种,因此要保持和ApiResult一致; 建议继承此基类,定义清楚错误返回码
    """
    def __init__(self, code, message, payload=None):
        super().__init__(code, message, payload)

    def to_dict(self):
        ret = dict()
        ret["code"] = self.code
        ret["message"] = self.message
        if not self.payload:
            ret.update(self.payload)
        return ret


class InnerException(BaseCustomException):
    def __init__(self, message):
        super().__init__(message, -1000, payload=None)


class InvalidException(BaseCustomException):
    def __init__(self, message, condition=None):
        super().__init__(message, -1001, payload={"condition": condition})


class NoSuchAppException(BaseCustomException):
    def __init__(self):
        super().__init__("No such application!", -2000, {"solution": "请 检查公钥填写是否正确 或 联系管理员开通应用."})


class NoPermException(BaseCustomException):
    def __init__(self):
        super().__init__("No permission!", -2001, {"solution": "请联系管理员 开通 或 提升 权限."})


class DiffSignatureException(BaseCustomException):
    def __init__(self, signature):
        super().__init__("Verify signature failed!", -3000, {"signature": f"服务端签名值: {signature}"})


class ExpiredTimestampException(BaseCustomException):
    def __init__(self, period):
        super().__init__("Expired timestamp found!", -3001, {"solution": f"有效期: {period}"})


class UnsupportedFormatException(BaseCustomException):
    def __init__(self, format):
        super().__init__("Unsupported format!", -1005, {"solution": f"格式: {format}"})
