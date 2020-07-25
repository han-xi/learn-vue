from flask import jsonify, Blueprint,request
from mongoClient import MongoDBClient233
import json
from datetime import datetime
import time
from functions import md5value
client = MongoDBClient233()


userUpdate = Blueprint('userUpdate', __name__)
@userUpdate.route('/userUpdate', methods=["PUT"])
def check_update():
    postdata = request.get_data()
    postdata = json.loads(postdata)
    try:
        user = client.info.find_one({"username":postdata["username"]})
        mail =client.mail.find_one({"tomail":postdata["username"]})
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
        elif postdata["smscode"]!=mail["code"]:
            return jsonify({
                "error":"验证码不正确"
            }),510
        if user != None:
            try:
                salt=user["salt"]   
                md5password=md5value(salt+postdata["password"])
                client.info.update({"username":postdata["username"]},{"$set":{"password":md5password}})
            except:
                return jsonify({#数据库连接失败用500表示
                }),500
            else:
                return jsonify({  
                })
        else:
            return jsonify({
                "error":"用户未注册",  
            }),401