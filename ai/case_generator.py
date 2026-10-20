import requests
from openai import OpenAI

PROMPT = """
你是资深接口测试工程师。以下是接口的 OpenAPI 定义：
{schema}

请为每一个接口设计测试用例，必须覆盖：
1. 正常流程
2. 参数边界（空值、超长、类型错误）
3. 业务异常（余额不足、重复提交、权限不足）
4. 安全风险（越权、无 token 访问）

【极其重要】输出格式必须严格遵守以下示例：

- name: 登录-正常
  request:
    method: POST
    path: /api/user/login
    json: {username: "load001", password: "123456"}
  assert:
    - {type: status, expected: 200}
    - {type: field, path: $.code, op: eq, expected: 0}

- name: 登录-无 token
  request:
    method: GET
    path: /api/user/info
  assert:
    - {type: status, expected: 401}

- name: 下单-正常
  request:
    method: POST
    path: /api/order/create
    headers: {token: "${token}"}
    json: {plan_id: "${plan_id}"}
  assert:
    - {type: status, expected: 200}
    - {type: field, path: $.code, op: eq, expected: 0}

【格式要求】
1. 断言类型只能是：status、field、db、schema
2. 操作符只能是：eq、neq、len_gt、contains、exists
3. path 必须是 JSONPath 格式，比如 $.code、$.data[0].user_id
4. token 统一用 "${token}"，plan_id 统一用 "${plan_id}"，注册用户统一用 "${tmp_user}"
5. 不要写 "a" * 1000 这种 YAML 不支持的表达式，直接写 200 个 a
6. 只输出 YAML，不要解释，总用例数不少于 40 条。
"""

def gen(path_schema, model="glm-4.7-flash"):
    client = OpenAI(
        api_key="3fa94bda08eb40c79d5733e188ccb575.3deQN7aY4yqD8JlE",
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    )
    # 不用 .format()，用 .replace()
    prompt_text = PROMPT.replace("{schema}", str(path_schema))
    r = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt_text}]
    )
    return r.choices[0].message.content

if __name__ == "__main__":
    schema = requests.get("http://127.0.0.1:8000/openapi.json").json()

    # 把整个 OpenAPI 文档发给大模型，让它生成所有接口的用例
    yaml_str = gen(schema)

    print(yaml_str)
    with open("cases/generated/all_api.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_str)