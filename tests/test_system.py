import uuid
import time
import json

from app.verify import signature_calc
from tests.base import BaseTest


class SystemTestCase(BaseTest):
    """
    System 测试用例
    """

    def test_application_crud(self):
        # 1.新增并返回查询结果
        # 1.1 构造待使用参数
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-Nonce": str(uuid.uuid4()),
            "X-Timestamp": int(round(time.time() * 1000)),
            "X-Access-Key": self.access_key,
            "X-Keys": "X-Nonce,X-Timestamp,X-Access-Key",
            "X-Signature": None,
        }
        body = {
            "name": "Tester",
            "desc": "This is a test account.",
            "owner": "TestTeam",
        }
        # 1.2 预期新增成功(需要签名)
        body_str = json.dumps(body)
        headers["X-Signature"] = signature_calc(self.access_key, self.secret_key, None, headers, body_str)
        resp = self.client.post("/openapi/apps", headers=headers, data=body_str)
        obj = resp.json
        self.expectSuccess(obj)
        # 1.3 验证数据是否正确
        self.assertIn("data", obj, "预期包含字段data.")
        self.assertIn("name", obj["data"], "预期resp['data']包含字段name.")
        self.assertEqual(obj["data"]["name"], "Tester", "预期字段resp['data']['name']值为'Tester'.")

        # 2.删除并查询确认
        # 2.1 截留记录编号
        self.assertIn("id", obj["data"], "预期resp['data']包含字段id.")
        app_id = obj["data"]["id"]
        # 2.2 预期删除成功
        headers["X-Signature"] = signature_calc(self.access_key, self.secret_key, None, headers, None)
        resp = self.client.delete(f"/openapi/apps/{app_id}", headers=headers)
        self.expectSuccess(resp.json)
        # 2.3 预期查询失败（已删除）
        headers["X-Signature"] = signature_calc(self.access_key, self.secret_key, None, headers, None)
        resp = self.client.get(f"/openapi/apps/{app_id}", headers=headers)
        self.expectFail(resp.json)
