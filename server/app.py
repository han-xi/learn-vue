from flask import Flask,g,request,session,redirect,jsonify,Response
from flask_cors import CORS
from mongoClient import MongoDBClient233
from flask import jsonify


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

from apis.user import user
from datetime import datetime
import config

app.config.from_pyfile('config.py',silent=True)
app.register_blueprint(user, url_prefix='/user')


@app.after_request
def after_request(response):
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    # 这里不能使用add方法，否则会出现 The 'Access-Control-Allow-Origin' header contains multiple values 的问题
    try:
        if g.token:#每次登录时设置token
            response.set_cookie('token',g.token,httponly=True,max_age=3600)
        if g.levelendtime:
            response.set_cookie('levelendtime',g.levelendtime,httponly=True,max_age=3600)

    except:
        pass
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
#ServerSelectionTimeoutError
@app.errorhandler(404)# 参数是错误代码
def error404(error_info):# 注意，一定要加参数接收错误信息 
    # 404 Not Found: The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.
    return jsonify({"error":'请求错误'})# 可以返回 三剑客 + 小儿子　@app.errorhandler(404)# 参数是错误代码
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9004, threaded=True, debug=True)
