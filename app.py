from flask import Flask, request, redirect, render_template
from urllib import parse
import requests
app = Flask(__name__)
# https://port-0-flask-108dypx2ale3vyt89.sel3.cloudtype.app/

@app.route("/")
def index():
    return render_template('./index.html')

@app.route("/auth", methods=['GET'])
def auth():
    auth_url = "https://openapi.swit.io/oauth/authorize"
    params = {
        "scope": "admin:read admin:write user:read user:write",
        "client_id": "Zp4yUGEvt4ewnqKW7ys4uvF17lTQImKg",
        "redirect_uri": "http://127.0.0.1:5000/auth/callback",
        "response_type": "code"
    }
    return redirect(f"{auth_url}?{parse.urlencode(params)}")

@app.route("/auth/callback", methods=['GET'])
def auth_callback():
    code = request.args.get("code")
    token_url = "https://openapi.swit.io/oauth/token"
    headers_obj = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data_obj = {
        "grant_type": "authorization_code",
        "client_id": "Zp4yUGEvt4ewnqKW7ys4uvF17lTQImKg",
        "client_secret": "6AZZE4g0260rG6K6AiI5lwSP",
        "redirect_uri": "http://127.0.0.1:5000/auth/callback",
        "code": code
    }
    response = requests.post(token_url, headers=headers_obj, data=data_obj)
    tk = response.json()["access_token"]
    print(tk)    
    with open('tokens.py', 'w') as f:
        f.write("user = '{}'".format(tk))
    return response.json()

@app.route("/test")
def test():
    import tokens as tk
    headers = {
        "Authorization": "Bearer "+ tk.user
    }

    response = requests.get(url="https://openapi.swit.io/v1/api/organization.user.list", headers=headers)
    return response.json()

# # slack webhook test
# @app.route("/webhook", methods=['POST'])
# def webhook():
#     # 앞에 필요없는 부분 슬라이스 (슬랙쪽 설정에 맞춰서 한 것이기 때문에 실제 구현때는 적절히 바꿀필요있음)
#     text = request.form.get("text")[7:]

#     # swit webhook endpoint
#     endpoint = "https://xxx.xxx/xxx"

#     # plain text 만 가능
#     json_data = {
#         "text": text
#     }

#     headers_data = {
#         'Content-type' : 'application/json'
#     }
#     res = requests.post(url=endpoint, json=json_data, headers=headers_data, timeout=180)

#     if res.ok:
#         # slack webhook 이용시 응답
#         response_text = "success"

#     response_text = "fail"

#     return {
#         "text": response_text
#     }
