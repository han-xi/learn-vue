from flask import jsonify, Blueprint,request
from mongoClient import MongoDBClient233
import json
client = MongoDBClient233()

updata = Blueprint('updata', __name__)
@updata.route('/updata', methods=["POST"])
def up():
    data = request.get_data()
    data = json.loads(data)
    #print(type(data))
    try:
        user = client.info.find_one({"username":data["username"]})
    except:
         return jsonify({
                "error":"数据库出现异常"
            }),503
    else:
        if user == None:
            try:
                client.info.insert(data)
            except:
                return jsonify({
                    "error":"数据库出现异常"
                }),503
            else:
                return jsonify({
                    "error":"注册成功",
                })
        else:
            return jsonify({
                "error":"用户已注册",   
            }),503


    

    