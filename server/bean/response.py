# -*- coding: UTF-8 -*-
# author:      Liu Kun
# email:       liukunup@outlook.com
# timestamp:   2022-09-10 23:01:00
# description: Response

__all__ = ["ApiResponse", "Success", "Failed"]

import json

from typing import Any, Text
from server.bean import BaseBean, Integer, Float


class ApiResponse(BaseBean):
    """ 通用接口响应类 """

    # 返回码 & 返回消息
    __code = None
    __message = None
    # 返回数据
    __payload = None
    # 调用耗时(单位: 毫秒)
    __time_elapsed_ms = None

    def __init__(self, code: Integer, message: Text, payload: Any = None, time_elapsed_ms: Float = None):
        super().__init__()
        self.__code = code
        self.__message = message
        self.__payload = payload
        self.__time_elapsed_ms = time_elapsed_ms

    @property
    def code(self) -> Integer:
        return self.__code

    @code.setter
    def code(self, code: Integer):
        self.__code = code

    @property
    def message(self) -> Text:
        return self.__message

    @message.setter
    def message(self, message: Text):
        self.__message = message

    @property
    def payload(self) -> Any:
        return self.__payload

    @payload.setter
    def payload(self, payload: Any):
        self.__payload = payload

    @property
    def time_elapsed_ms(self) -> Float:
        return self.__time_elapsed_ms

    @time_elapsed_ms.setter
    def time_elapsed_ms(self, time_elapsed_ms: Float):
        self.__time_elapsed_ms = time_elapsed_ms

    def data(self):
        resp_obj = dict()
        resp_obj.setdefault("code", self.__code)
        resp_obj.setdefault("message", self.__message)
        if self.__payload:
            resp_obj.setdefault("payload", self.__payload)
        if self.__time_elapsed_ms:
            resp_obj.setdefault("timeElapsedMs", self.__time_elapsed_ms)
        return resp_obj

    def __repr__(self):
        return json.dumps(self.data(), ensure_ascii=False, indent=4, separators=(",", ":"), sort_keys=True)

    def __str__(self):
        return json.dumps(self.data())


class Success(ApiResponse):
    """ 成功 """

    def __init__(self, payload: Any = None, time_elapsed_ms: Float = None):
        super().__init__(200, "success", payload=payload, time_elapsed_ms=time_elapsed_ms)


class Failed(ApiResponse):
    """ 失败 """

    def __init__(self, payload: Any = None, time_elapsed_ms: Float = None):
        super().__init__(-1, "failed", payload=payload, time_elapsed_ms=time_elapsed_ms)
