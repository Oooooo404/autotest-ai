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

@pytest.mark.parametrize("case", load_all_cases())
def test_api(case, tmp_user):
    headers = case["request"].get("headers", {})
    json_data = case["request"].get("json", {})
    # 如果 json 是 "${tmp_user}"，就用 fixture 的数据替换
    if json_data == "${tmp_user}":
        json_data = tmp_user
    resp = Client().req(case["request"]["method"], case["request"]["path"],
                        headers=headers, json=json_data)
    do_assert(resp, case["assert"])