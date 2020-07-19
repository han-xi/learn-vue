from flask import Flask,request,session,redirect,jsonify,url_for
from flask_cors import CORS

from flask import jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

from loaddata import loaddata
from updata import updata
from mail import mail
# from search import search
app.register_blueprint(loaddata, url_prefix='/')
app.register_blueprint(updata, url_prefix='/')
app.register_blueprint(mail, url_prefix='/')
app.secret_key='\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
# @app.route('/')
# def wapper(func):
#     def inner(*args,**kwargs):
#         if not session.get('user_info'):
#             return redirect('/PersonalCenterLogin')
#         return func(*args,**kwargs)
#     return inner

# app.register_blueprint(search, url_prefix='/search')
@app.before_request#执行所有装饰器都要执行当前装饰器(简洁版实现同样功能)
def login_required():
    if request.path in ['/loaddata']: #如果登录的路由是注册和登录就返会none
        return None
    user=session.get('user_id')  #获取用户登录信息
    if not user:                 #没有登录就自动跳转到登录页面去
        #print("-------")
        return redirect(url_for('login'))
    return None
@app.route('/login/', methods=['GET', 'POST'])
def login():
    print("----------")
    return jsonify({"error":"/PersonalCenterLogin"}),302
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9004, threaded=True, debug=True)
