&#x20;AutoTest-AI 智能接口自动化测试平台



&#x20;1.项目简介

基于 Python + pytest + requests 搭建的数据驱动接口自动化测试框架，用于对 `vip-mini` 靶子系统进行全链路接口回归测试。框架集成了动态造数、多类型断言、Mock 服务以及大模型（LLM）辅助生成用例能力，并接入了 GitHub Actions CI。



&#x20;2.技术栈

\- 语言：Python 3.11

\- 框架：pytest、requests

\- 数据驱动：YAML、PyYAML

\- 断言引擎：jsonpath-ng、jsonschema、pymysql

\- 造数：Faker

\- AI 辅助：智谱 GLM 大模型 API

\- 持续集成：GitHub Actions、Docker



3\. 目录结构

autotest-ai/

├── ai/                AI 辅助生成用例脚本 (read\_swagger.py, case\_generator.py)

├── cases/             测试用例 (test\_yaml.py 驱动 data/ 下的 YAML)

│   └── data/          YAML 用例文件 (手工编写 + AI 生成)

├── core/              核心引擎 (client.py 封装, assertion.py 断言, config.py 配置)

├── mock/              Flask Mock 服务 (模拟支付回调超时/异常)

├── docs/              测试报告与文档

├── conftest.py        pytest fixtures (动态获取 token, plan\_id, order\_id, tmp\_user)

├── config.yaml        多环境配置 (test 环境 / docker 环境)

└── Dockerfile         镜像化配置文件



4\.核心功能与亮点

1）全动态数据获取：用例中不写死任何业务数据。通过 conftest.py 中的 fixture，自动登录获取 token、查询套餐获取 plan\_id、下单获取 order\_id，并用 Faker 随机生成 tmp\_user，测试后自动清理数据，保证用例互不干扰。

2）多类型断言引擎：支持 HTTP 状态码断言 (status)、JSONPath 字段断言 (field)、数据库落库校验 (db) 以及 JSON Schema 结构断言 (schema)。

3）Mock 异常场景：基于 Flask 搭建 Mock 服务，模拟第三方支付回调的超时 (timeout) 和异常 (error)，验证系统的兜底逻辑。

4）AI 辅助生成用例：读取 Swagger (/openapi.json) 接口定义，调用大模型自动生成 YAML 格式的异常和边界用例。经过人工校准后入库。

5）CI/CD 与镜像化：基于 Dockerfile 实现环境一键部署；接入 GitHub Actions 实现 push 触发与每日定时回归。



5\.快速开始

1）启动被测系统 (确保 Docker 和 vip-mini 已启动)

uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

2）运行全量测试

pytest cases/ -v

3）Docker 镜像化运行

docker build -t autotest-ai .

docker run autotest-ai



6\.落地效果与数据

\- 接入接口：10 个核心接口。

\- 用例总数：55 条（手工编写 17 条 + AI 生成并人工校准 38 条）。

\- AI 生成保留率：约 90%（大模型生成 42 条，人工剔除 3 条重复的边界用例及 1 条签名传参错误的用例，正式入库 38 条）。

\- 缺陷发现：全量执行后，发现 10 条失败用例。经人工排查，这 10 条 100% 均为靶子系统真实缺陷（例如：空密码可登录、负数可加积分、超长参数导致 500 崩溃、同分排序错误等），已全部登记至 `vip-mini` 的 GitHub Issues。

\- 执行效率：单次全量回归耗时约 6 秒；环境准备耗时由手工搭建的 2 小时 降至 Docker 一键启动的 15 秒。

