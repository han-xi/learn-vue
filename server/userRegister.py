from flask import jsonify, Blueprint,request
from mongoClient import MongoDBClient233
import json
from datetime import datetime
import time
from functions import md5value,genRandomString

client = MongoDBClient233()


userRegister = Blueprint('userRegister', __name__)
@userRegister.route('/userRegister', methods=["POST"])
def check_register():
    postuserinfo = request.get_data()
    postuserinfo = json.loads(postuserinfo)
    try:
        user = client.info.find_one({"username":postuserinfo["username"]})
        mail =client.mail.find_one({"tomail":postuserinfo["username"]})
    except:
         return jsonify({#数据库连接失败用500表示
            }),500
    else:
        nowtime = datetime.now() #获得当前时间
        if mail == None:#没有点击验证码的情况使得初始为空
            return jsonify({
                "error":"请点击发送按钮进行发送"
            }),510
        elif (nowtime-mail["maildate"]).seconds >= 600: #验证码超时十分钟
            return jsonify({
                "error":"验证码超时"
            }),510
        elif postuserinfo["smscode"]!=mail["code"]:
            return jsonify({
                "error":"验证码不正确"
            }),510
        if user == None:
            try:
                salt=genRandomString()
                md5password=md5value(salt+postuserinfo["password"])
                userinfo={}
                userinfo.update({"username":postuserinfo["username"]})
                userinfo.update({"password":md5password})
                userinfo.update({"registerdate":nowtime})
                userinfo.update({"salt":salt})
                client.info.insert(userinfo)
            except:
                return jsonify({#数据库连接失败用500表示
                }),500
            else:
                return jsonify({  
                })
        else:
            return jsonify({
                "error":"用户已注册",
            }),401  