import time
from flask import Flask,request

app = Flask(__name__)

@app.post("/mock/pay/callback")
def pay():
    mode = request.args.get("mode","ok")
    if mode == "timeout":
        time.sleep(30)
        return {"code":0}
    if mode == "error":
        return {"code":500,"msg":"sign invalid"},500
    return {"code":0,"msg":"success"}

if __name__ == "__main__":
    app.run(port=9000)