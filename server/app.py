from flask import Flask,g,request,session,redirect,jsonify,Response
from flask_cors import CORS
from mongoClient import MongoDBClient233
from flask import jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

from apis.user import user
import datetime

app.register_blueprint(user, url_prefix='/user')
app.secret_key='\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
app.permanent_session_lifetime=datetime.timedelta(days=14)

@app.before_request#执行所有装饰器都要执行当前装饰器(简洁版实现同样功能)
def login_required():
    if request.path in ['/user/login','/user/register','/user/forget','/user/active','/user/changepassword']: #如果登录的路由是注册和登录就返会none
        return None    
    try:
        username=session.get('user_id')  #获取用户登录信息
    except:
        return jsonify(''),400
    if username :
        g.username=username
        return None
    # if  username :                 #没有登录就自动跳转到登录页面去
    #     g.username=username
    #     return None 
    # elif userinfo['islogin']==True:#失效就更改登录标志
    #     client.info.update({"username":g.username},{"$set":{"islogin":False}})
    #     return jsonify({"errCode":2}),401
    else:
        return jsonify({"errCode":2}),401


@app.after_request
def after_request(response):
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    # 这里不能使用add方法，否则会出现 The 'Access-Control-Allow-Origin' header contains multiple values 的问题
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9004, threaded=True, debug=True)
