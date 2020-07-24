from flask import jsonify, Blueprint,request
from mongoClient import MongoDBClient233
import json
from datetime import datetime
import time
import random,string
import hashlib
def genRandomString(slen=10):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))
def md5value(s):
    md5 = hashlib.md5()
    md5.update(s.encode())
    return md5.hexdigest()
client = MongoDBClient233()


userRegister = Blueprint('userRegister', __name__)
@userRegister.route('/userRegister', methods=["POST"])
def check_register():
    data = request.get_data()
    data = json.loads(data)
    try:
        user = client.info.find_one({"username":data["username"]})
        mail =client.mail.find_one({"tomail":data["username"]})
    except:
         return jsonify({#数据库连接失败用500表示
            }),500
    else:
        nowtime = datetime.now() #获得当前时间
        #print(type(mail["maildate"]))
        print(type(nowtime))
        if mail == None:#没有点击验证码的情况使得初始为空
            return jsonify({
                "error":"请点击发送按钮进行发送"
            }),510
        elif (nowtime-mail["maildate"]).seconds >= 600: #验证码超时十分钟
            return jsonify({
                "error":"验证码超时"
            }),510
        elif data["smscode"]!=mail["code"]:
            return jsonify({
                "error":"验证码不正确"
            }),510
        if user == None:
            try:
                salt=genRandomString()
                #print("221")
                #print(type(data["password"]))
                
                md5password=md5value(salt+data["password"])
                #print(md5password)
                #print("--")
                userinfo={}
                userinfo.update({"username":data["username"]})
                userinfo.update({"password":md5password})
                userinfo.update({"registerdate":nowtime})
                print("22")
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