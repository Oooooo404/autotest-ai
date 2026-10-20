import requests
import json

schema = requests.get("http://127.0.0.1:8000/openapi.json").json()

for path,item in schema["paths"].items():
    for method,detail in item.items():
        print(method.upper(),path,detail.get("summary"))