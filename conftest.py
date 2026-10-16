import pytest
from core.client import Client

@pytest.fixture(scope="session")
def token():
    r = Client().json("POST", "/api/user/login", json={"username": "load001", "password": "123456"})
    return r["token"]

@pytest.fixture()
def cli(token):
    return Client(token)

@pytest.fixture()
def tmp_user():
    """生成临时用户，测试后自动清理"""
    from core.data_factory import new_user
    from db_helper import query

    u = new_user()
    yield u
    #测试后清理
    query("DELETE FROM user WHERE username=%s",(u["username"],))