import pymysql
from core.config import load

def query(sql,args=()):
    """执行SQL，返回结果"""
    db = load()["db"]
    c = pymysql.connect(
        host=db["host"],port=db["port"],user=db["user"],
        password=db["password"],database=db["db"],
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with c.cursor() as cur:
            cur.execute(sql,args)
            r = cur.fetchall()
            c.commit()
            return r
    finally:
        c.close()