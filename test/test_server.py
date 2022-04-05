import os
import tempfile
import pytest
import logging
import uuid
import time
import hashlib
import hmac
import json

from server import create_app

log = logging.getLogger(__name__)


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(os.getenv("FLASK_CONFIG") or "test")
    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_user(client):
    # 新增
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    body = {
        "nickname": "Tester",
        "username": "tester",
    }
    resp = client.post("/openapi/users", headers=headers, json=body)
    obj = resp.json
    assert obj["code"] == 200
    assert obj["data"]["nickname"] == "Tester"
    assert obj["data"]["username"] == "tester"
    # 查询
    resp = client.get(f"/openapi/users/{obj['data']['id']}")
    obj = resp.json
    uid = obj["data"]["id"]  # 记录下来 删除时已经不会再返回
    assert obj["code"] == 200
    assert obj["data"]["nickname"] == "Tester"
    assert obj["data"]["username"] == "tester"
    # 删除
    resp = client.delete(f"/openapi/users/{uid}")
    obj = resp.json
    assert obj["code"] == 200
    # 查询（确认已删除）
    resp = client.get(f"/openapi/users/{uid}")
    obj = resp.json
    assert obj["code"] == -1


def test_app(client):
    # Admin App
    access_key = "jT4xWw9VyHE6saur5Ol173RYoQCcGIFi"
    secret_key = "5JAYvGeXNxzD26a4QRocE7rpyO9ST13m"
    # 新增
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "X-Nonce": str(uuid.uuid4()),
        "X-Timestamp": int(round(time.time() * 1000)),
        "X-AccessKey": access_key,
        "X-Signature": None,
    }
    body = {
        "name": "Tester",
        "desc": "This is a test account.",
        "owner": "TestTeam",
    }
    headers["X-Signature"] = sign(access_key, secret_key, None, headers, body)
    resp = client.post("/openapi/apps", headers=headers, data=json.dumps(body))
    obj = resp.json
    assert obj["code"] == 200
    assert obj["data"]["name"] == "Tester"
    # 查询
    headers["X-Signature"] = sign(access_key, secret_key, None, headers, None)
    resp = client.get(f"/openapi/apps/{obj['data']['id']}", headers=headers)
    obj = resp.json
    uid = obj["data"]["id"]  # 记录下来 删除时已经不会再返回
    assert obj["code"] == 200
    assert obj["data"]["name"] == "Tester"
    # 删除
    headers["X-Signature"] = sign(access_key, secret_key, None, headers, None)
    resp = client.delete(f"/openapi/apps/{uid}", headers=headers)
    obj = resp.json
    assert obj["code"] == 200
    # 查询（确认已删除）
    headers["X-Signature"] = sign(access_key, secret_key, None, headers, None)
    resp = client.get(f"/openapi/apps/{uid}", headers=headers)
    obj = resp.json
    assert obj["code"] == -1


def sign(access_key, secret_key, params, headers, body):
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
    #
    headers.pop("X-Signature")
    #
    content_list = list()
    if params is not None and isinstance(params, dict):
        content_list.extend([str(dat[1]) for dat in sorted(params.items(), key=lambda kv:kv[0])])
    if headers is not None and isinstance(headers, dict):
        content_list.extend([str(dat[1]) for dat in sorted(headers.items(), key=lambda kv: kv[0])])
    if body is not None and isinstance(body, dict):
        content_list.append(json.dumps(body))
    if body is not None and isinstance(body, str):
        content_list.append(body)
    content_list.append(secret_key)
    content = ";".join(content_list)
    return hmac.new(bytes(access_key, encoding="utf-8"), bytes(content, encoding="utf-8"),
                    digestmod=hashlib.sha256).hexdigest().lower()
