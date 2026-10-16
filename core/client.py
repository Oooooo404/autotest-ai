import requests
from core.config import load

CFG = load()

class Client:
    def __init__(self,token=None):
        self.s = requests.Session()
        self.token = token

    def req(self,method,path,**kw):
        url = CFG["base_url"] + path
        headers = kw.pop("headers",{})
        if self.token:
            headers["token"] = self.token
        r = self.s.request(method,url,headers=headers,timeout=10,**kw)
        return r

    def json(self,*a,**kw):
        return self.req(*a,**kw).json()

