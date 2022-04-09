from tests.base import BaseTest


class StudentTestCase(BaseTest):
    """
    Student 测试用例
    """

    def test_student_crud(self):
        # 1.新增并返回查询结果
        # 1.1 构造待使用参数
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }
        body = {
            "name": "ZhangSan",
        }
        # 1.2 预期新增成功
        resp = self.client.post("/openapi/students", headers=headers, json=body)
        obj = resp.json
        self.expectSuccess(obj)
        # 1.3 验证数据是否正确
        self.assertIn("data", obj, "预期包含字段data.")
        self.assertIn("name", obj["data"], "预期resp['data']包含字段name.")
        self.assertEqual(obj["data"]["name"], "ZhangSan", "预期字段resp['data']['name']值为'ZhangSan'.")

        # 2.更新数据并查询验证
        # 2.1 截留记录编号
        self.assertIn("id", obj["data"], "预期resp['data']包含字段id.")
        stu_id = obj["data"]["id"]
        # 2.2 预期更新成功
        body.clear()
        body = {
            "name": "LiSi",
            "sex": "Female",
        }
        resp = self.client.put(f"/openapi/students/{stu_id}", headers=headers, json=body)
        obj = resp.json
        self.expectSuccess(obj)
        # 2.3 验证数据是否正确
        self.assertIn("data", obj, "预期包含字段data.")
        # 验证 name
        self.assertIn("name", obj["data"], "预期resp['data']包含字段name.")
        self.assertEqual(obj["data"]["name"], "LiSi", "预期字段resp['data']['name']值为'LiSi'.")
        # 验证 sex
        self.assertIn("sex", obj["data"], "预期resp['data']包含字段sex.")
        self.assertEqual(obj["data"]["sex"], "Female", "预期字段resp['data']['sex']值为'Female'.")

        # 3.删除并查询确认
        # 3.1 截留记录编号
        self.assertIn("id", obj["data"], "预期resp['data']包含字段id.")
        stu_id = obj["data"]["id"]
        # 3.2 预期删除成功
        resp = self.client.delete(f"/openapi/students/{stu_id}", headers=headers)
        self.expectSuccess(resp.json)
        # 3.3 预期查询失败（已删除）
        resp = self.client.get(f"/openapi/students/{stu_id}", headers=headers)
        self.expectFail(resp.json)
