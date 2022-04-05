import copy
import datetime
import hashlib
import hmac

from flask import request
from . import db
from .model.system import App
from .exceptions import *


def permission_verify(permission):
    """
    权限验证
    :param permission: 权限枚举值
    :return: 不涉及(当验证失败时抛出异常)
    """
    # 获取请求头字典
    headers = request.headers
    # 检查公钥参数是否合法
    if "X-AccessKey" not in headers or headers["X-AccessKey"] is None or len(headers["X-AccessKey"]) != 32:
        raise InvalidException("字段 X-AccessKey 配置问题!",
                               condition="定长32个字符; 来自已配置的数据库 app 表 secret_key 字段.")
    # 根据公钥查询App
    app = db.session.query(App).filter(App.access_key == headers["X-AccessKey"]).first()
    # 检查 公钥 是否存在
    if app is None:
        raise NoSuchAppException()
    # 检查 权限 是否允许
    if not app.can(permission):
        raise NoPermException()


def signature_verify():
    """
    签名验证
    :return: 不涉及(当验证失败时抛出异常)
    """
    # 请求头字段字典
    headers = dict(request.headers)

    # 检查 时间戳 参数是否合法
    if "X-Timestamp" not in headers or headers["X-Timestamp"] is None:
        raise InvalidException("字段 X-Timestamp 未配置!", condition="格式: %Y-%m-%d %H:%M:%S %Z %z")
    # 验证时间戳是否有效
    timestamp = headers["X-Timestamp"]
    if not timestamp_verify(timestamp):
        raise ExpiredTimestampException("10分钟")

    # 检查 公钥 参数是否合法
    if "X-Accesskey" not in headers or headers["X-Accesskey"] is None or len(headers["X-Accesskey"]) != 32:
        raise InvalidException("字段 X-AccessKey 未配置或存在配置问题!",
                               condition="定长32个字符; 来自已配置的数据库 app 表 secret_key 字段.")
    # 检查 公钥 是否存在
    access_key = headers["X-Accesskey"]
    app = db.session.query(App).filter(App.access_key == access_key).first()
    if app is None:
        raise NoSuchAppException()

    # 检查 签名 参数是否合法
    if "X-Signature" not in headers or headers["X-Signature"] is None:
        raise InvalidException("字段 X-Signature 未配置!", condition="签名方法请参考 README.md 文档.")
    # 服务端计算签名值
    local_signature = signature_calc(app.access_key, app.secret_key, request.args, headers, request.data)
    # 校验签名是否一致
    signature = headers["X-Signature"]
    if signature != local_signature:
        raise DiffSignatureException(local_signature)


def signature_calc(access_key, secret_key, params, headers, body):
    """
    签名计算
    签名方法请参考 README.md 文档
    :param access_key: 公钥
    :param secret_key: 私钥
    :param params:     路径参数
    :param headers:    请求头参数
    :param body:       请求体内容
    :return: 签名值
    """
    # 计算时务必去除 X-Signature 字段
    tmp_headers = copy.deepcopy(headers)
    for item in ["X-Signature", "User-Agent", "Host", "Content-Length"]:
        if item in tmp_headers:
            tmp_headers.pop(item)
    #
    content_list = list()
    if params is not None and isinstance(params, dict):
        content_list.extend([str(dat[1]) for dat in sorted(params.items(), key=lambda kv:kv[0])])
    if tmp_headers is not None and isinstance(tmp_headers, dict):
        content_list.extend([str(dat[1]) for dat in sorted(tmp_headers.items(), key=lambda kv: kv[0])])
    if body is not None and isinstance(body, bytes) and len(body) > 0:
        content_list.append(body.decode())
    content_list.append(secret_key)
    content = ";".join(content_list)
    return hmac.new(bytes(access_key, encoding="utf-8"), bytes(content, encoding="utf-8"),
                    digestmod=hashlib.sha256).hexdigest().lower()


def timestamp_verify(timestamp, period=10):
    """
    时间戳验证有效期
    :param timestamp: 待验证的毫秒时间戳
    :param period:    有效期时长(单位: 分钟; 默认10分钟)
    :return: 是否在有效期内
    """
    try:
        target = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
        now = datetime.datetime.now()
        return now - datetime.timedelta(minutes=period) <= target <= now + datetime.timedelta(minutes=period)
    except Exception as e:
        print(e)
        raise UnsupportedFormatException("")
