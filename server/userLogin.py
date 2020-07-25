from flask import jsonify, Blueprint,request,session
from mongoClient import MongoDBClient233
import json
from functions import md5value
client = MongoDBClient233()
userLogin = Blueprint('userLogin', __name__)
@userLogin.route('/userLogin', methods=["POST"])

def check_login():
    userinfo = request.get_data()
    userinfo = json.loads(userinfo)
    try: 
        db_userinfo = client.info.find_one({"username":userinfo['username']})
    except:
        return jsonify({
        }), 500
    else:
        if db_userinfo == None:
            return jsonify({
                'error': "未发现用户.",
            }), 401
        else:
            if md5value(db_userinfo["salt"]+userinfo['password'])== db_userinfo["password"]:
                session['user_id']=userinfo['username']
                session.permanent = True
                del db_userinfo["_id"]
                temp={}
                temp.update({"errCode":3})
                #temp.update({"token":userdata["token"]})
                return jsonify(temp)
            else:
                return jsonify({
                'error': "密码错误.",
                }), 401