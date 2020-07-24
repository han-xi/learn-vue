from flask import Flask,request,session,redirect,jsonify,url_for,abort,Response
from flask_cors import CORS

from flask import jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

from userLogin import userLogin
from userRegister import userRegister
from userMail import userMail
import datetime
# from search import search
app.register_blueprint(userLogin, url_prefix='/')
app.register_blueprint(userRegister, url_prefix='/')
app.register_blueprint(userMail, url_prefix='/')
app.secret_key='\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
app.permanent_session_lifetime=datetime.timedelta(days=14)

@app.before_request#执行所有装饰器都要执行当前装饰器(简洁版实现同样功能)
def login_required():
    #request.cookies
    if request.path in ['/userLogin','/userRegister','/userMail']: #如果登录的路由是注册和登录就返会none
        return None
    print("------")
    #name=request.cookies.get("u_uuid")
    #print(name)
    #print(session['user_id'])
    #print(session.getId())
    user=session.get('user_id')  #获取用户登录信息
    if  user  :                 #没有登录就自动跳转到登录页面去
       return None 
    return jsonify({"errCode":2}),401

@app.after_request
def after_request(response):
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    # 这里不能使用add方法，否则会出现 The 'Access-Control-Allow-Origin' header contains multiple values 的问题
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9004, threaded=True, debug=True)
