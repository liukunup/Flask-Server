# -*- coding: UTF-8 -*-
# author:      Liu Kun
# email:       liukunup@outlook.com
# timestamp:   2022/9/10 23:45
# description: Authentication

__all__ = ["signature_required", "permission_required", "admin_required"]

import datetime
import hashlib
import hmac

from flask import request
from typing import Text, Dict
from functools import wraps
from cachetools import cached, TTLCache, LRUCache
from server.bean import Bytes
from server.bean.error import InvalidParamException, NoPermissionException, DiffSignatureException
from server.model.rbca import Permission, MachineUser


def signature_required(f):
    """ 要求接口签名 """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = Authentication(request.args, request.headers, request.data)
        auth.verify_signature()
        return f(*args, **kwargs)
    return decorated


def permission_required(permission: Permission):
    """ 要求接口具备指定权限 """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = Authentication(request.args, request.headers, request.data)
            auth.verify_permission(permission)
            return f(*args, **kwargs)
        return decorated
    return decorator


def admin_required(f):
    """ 要求接口具备超级管理员权限 """
    return permission_required(Permission.ADMIN)(f)


class Authentication:
    """ 鉴权模块 """

    # HTTP/HTTPS 请求内容
    __params = None
    __headers = None
    __body = None

    def __init__(self, params, headers, body):
        self.__case_ignore(params, headers)
        self.__body = body

    def __case_ignore(self, params, headers):
        """ 忽略请求中的大小写差异 """
        # Params
        if isinstance(params, dict):
            self.__params = dict()
            for k, v in params.items():
                self.__params.setdefault(str(k).lower(), v)
        # Headers
        if isinstance(headers, dict):
            self.__headers = dict()
            for k, v in headers.items():
                self.__headers.setdefault(str(k).lower(), v)

    def verify_permission(self, permission: Permission):
        """ 验证权限 """
        # 检查公钥参数是否合法
        key = "X-Access-Key".lower()
        if key not in self.__headers or not isinstance(self.__headers[key], str) or len(self.__headers[key]) != 32:
            raise InvalidParamException(error="字段 X-Access-Key 未配置或存在配置问题", value=self.__headers.get(key),
                                        suggestions=["1.定长32字符", "2.来自已配置的数据库 machine_user.access_key 字段"])
        # 根据公钥查询App
        machine_user = self.__get_machine_user(self.__headers.get(key))
        # 检查 公钥 是否存在
        if not machine_user:
            raise InvalidParamException(error="访问密钥不存在", value=self.__headers.get(key),
                                        suggestions=["1.请检查字段 X-Access-Key 填写是否正确", "2.请联系管理员添加访问密钥"])
        # 检查 权限 是否允许
        if not machine_user.can(permission):
            raise NoPermissionException(error="无权访问此接口", value=permission,
                                        suggestions=["请联系管理员提升权限"])

    def verify_signature(self, valid_period_min=15):
        """ 验证签名 """
        # 检查 时间戳 参数是否合法
        key1 = "X-Timestamp".lower()
        if key1 not in self.__headers or not isinstance(self.__headers[key1], (int, float)):
            raise InvalidParamException(error="字段 X-Timestamp 未配置或存在配置问题", value=self.__headers.get(key1),
                                        suggestions=["1.整型或浮点型的毫秒时间戳", "2.与服务器保持时区一致"])
        # 验证时间戳是否有效
        if not self.__verify_timestamp(self.__headers.get(key1), valid_period_min=valid_period_min):
            raise InvalidParamException(error="请求已过期", value=self.__headers.get(key1),
                                        suggestions=[f"1.请求有效期{valid_period_min}分钟", "2.与服务器保持时区一致"])

        # 检查公钥参数是否合法
        key2 = "X-Access-Key".lower()
        if key2 not in self.__headers or not isinstance(self.__headers[key2], str) or len(self.__headers[key2]) != 32:
            raise InvalidParamException(error="字段 X-Access-Key 未配置或存在配置问题", value=self.__headers.get(key2),
                                        suggestions=["1.定长32字符", "2.来自已配置的数据库 machine_user.access_key 字段"])
        # 根据公钥查询App
        machine_user = self.__get_machine_user(self.__headers.get(key2))
        # 检查 公钥 是否存在
        if not machine_user:
            raise InvalidParamException(error="访问密钥不存在", value=self.__headers.get(key2),
                                        suggestions=["1.请检查字段 X-Access-Key 填写是否正确", "2.请联系管理员添加访问密钥"])

        # 检查 签名 参数是否合法
        key3 = "X-Signature".lower()
        if key3 not in self.__headers or not isinstance(self.__headers[key3], str) or len(self.__headers[key3]) == 0:
            raise InvalidParamException(error="字段 X-Signature 未配置或存在配置问题", value=self.__headers.get(key3),
                                        suggestions=["请参考 README.md 文档"])
        # 服务端计算签名值
        local_signature = self.calculate_signature(machine_user.access_key, machine_user.secret_key,
                                                   self.__params, self.__headers, self.__body)
        # 校验签名是否一致
        if self.__headers.get(key3) != local_signature:
            raise DiffSignatureException(error="客户端提交的签名与服务端本地计算不一致", value=local_signature,
                                         suggestions=["请参考 README.md 文档"])

    @staticmethod
    @cached(cache=LRUCache(maxsize=128))
    def calculate_signature(access_key: Text, secret_key: Text, params: Dict, headers: Dict, body: Bytes, debug=False):
        """
        签名计算
        签名方法请参考 README.md 文档
        :param access_key: 公钥
        :param secret_key: 私钥
        :param params:     路径参数
        :param headers:    请求头
        :param body:       请求体
        :param debug:      调试开关(默认关闭)
        :return: 签名值
        """
        # 待用来计算签名值的字段值列表
        content_list = list()
        # 路径参数
        if params:
            content_list.extend([str(e[1]) for e in sorted(params.items(), key=lambda kv: kv[0])])
        # 请求头
        key = "X-Keys".lower()
        if key not in headers or not isinstance(headers[key], str) or len(headers[key]) == 0:
            raise InvalidParamException(error="字段 X-Keys 未配置", value=headers.get(key),
                                        suggestions=["请参考 README.md 文档"])
        for k in headers["X-Keys"].split(","):
            content_list.append(str(headers.get(k)))
        # 请求体
        if body:
            content_list.append(body.decode(encoding="utf-8"))
        # 公钥
        content_list.append(access_key)
        # 连接成字符串
        content = ";".join(content_list)
        # 调试打印日志
        if debug:
            print(content)
        # 处理加密: 私钥 + 内容
        return hmac.new(bytes(secret_key, encoding="utf-8"), bytes(content, encoding="utf-8"),
                        digestmod=hashlib.sha256).hexdigest().lower()

    @staticmethod
    def __verify_timestamp(timestamp, valid_period_min=15):
        """ 验证时间戳 """
        try:
            target = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
            now = datetime.datetime.now()
            delta = valid_period_min
            return now - datetime.timedelta(minutes=delta) <= target <= now + datetime.timedelta(minutes=delta)
        except Exception as e:
            raise InvalidParamException(error=e.__str__(), value=timestamp,
                                        suggestions=["1.整型或浮点型的毫秒时间戳", "2.与服务器保持时区一致"])

    @staticmethod
    @cached(cache=TTLCache(maxsize=128, ttl=180))
    def __get_machine_user(access_key: Text):
        """ 根据AccessKey查询机器用户 """
        return MachineUser.query.filter_by(access_key=access_key).first()
