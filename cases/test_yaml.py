import yaml
import pytest
from core.client import Client
from core.assertion import do_assert

def load_all_cases():
    import os
    cases = []
    data_dir = "cases/data"
    for f in os.listdir(data_dir):
        if f.endswith(".yaml"):
            data = yaml.safe_load(open(f"{data_dir}/{f}",encoding="utf-8"))
            cases.extend(data)
    return cases

@pytest.mark.parametrize("case",load_all_cases())
def test_api(case):
    resp = Client().req(case["request"]["method"],case["request"]["path"],
                        headers=case["request"].get("headers",{}),
                        json=case["request"].get("json",{}))
    do_assert(resp,case["assert"])

@pytest.mark.parametrize("case",load_all_cases())
def test_api(case,token,plan_id,order_id,tmp_user):
    # 1.取出headers和json
    headers = case["request"].get("headers",{})
    json_data = case["request"].get("json",{})
    path = case["request"]["path"]

    # 2.如果 headers 里的 token 是 "${token}"，用 fixture 的 token 替换
    if headers.get("token") == "${token}":
        headers["token"] = token

    # 3. 如果 json 是 "${tmp_user}"，用 fixture 的数据替换
    if json_data == "${tmp_user}":
        json_data = tmp_user

    if json_data.get("plan_id") == "${plan_id}":
        json_data["plan_id"] = plan_id

    if "${order_id}" in path:
        path = path.replace("${order_id}",str(order_id))

    # 4.发请求
    resp = Client().req(case["request"]["method"],path,
                        headers=headers,json=json_data)

    # 5.执行断言
    do_assert(resp,case["assert"])