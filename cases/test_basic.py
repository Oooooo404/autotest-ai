from core.client import Client

def test_plan_list():
    r = Client().json("GET","/api/plan/list")
    assert r["code"] == 0
    assert len(r["data"]) >= 2