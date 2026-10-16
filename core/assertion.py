import yaml
import jsonschema
import pymysql
from jsonpath_ng import parse
from core.config import load

def _field(resp, a):
    """字段断言：用 JSONPath 提取字段，按 op 比较"""
    v = parse(a["path"]).find(resp.json())[0].value
    exp = a.get("expected")   # exists 不需要 expected，用 .get 取不到就是 None
    op = a["op"]

    ops = {
        "eq":       lambda: v == exp,
        "neq":      lambda: v != exp,
        "len_gt":   lambda: len(v) > exp,
        "contains": lambda: exp in v,
        "exists":   lambda: v is not None,
        "lt":       lambda: v < exp,
    }

    assert ops[op](), f"断言失败: path={a['path']}, op={op}, 实际值={v}, 期望值={exp}"

def _status(resp,a):
    """状态码断言"""
    assert resp.status_code == a["expected"],f"状态码{resp.status_code} != {a['expected']}"

def _db(resp,a):
    """数据库断言：查库，比对结果"""
    db = load()["db"]
    c = pymysql.connect(
        host=db["host"],port=db["port"],user=db["user"],
        password=db["password"],database=db["db"],
        cursorclass=pymysql.cursors.DictCursor
    )
    with c.cursor() as cur:
        cur.execute(a["sql"])
        v = cur.fetchone()
    c.close()
    assert v and float(list(v.values())[0]) == float(a["expected"]), f"DB 校验失败: {v}"

def _schema(resp,a):
    """JSON Schema 断言：校验响应结构"""
    schema = yaml.safe_load(open(a["file"],encoding="utf-8"))
    jsonschema.validate(resp.json(),schema)

def _not_empty(resp,a):
    """检查字段非空"""
    v = parse(a["path"]).find(resp.json())[0].value
    assert v,f"{a['path']} 为空"

ASSERTORS = {
    "status": _status,
    "field": _field,
    "db": _db,
    "schema": _schema,
    "not_empty": _not_empty,
}

def do_assert(resp,asserts):
    """便利断言列表，逐条执行"""
    for a in asserts:
        ASSERTORS[a["type"]](resp,a)