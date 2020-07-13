from flask import jsonify, Blueprint,request
from mongoClient import MongoDBClient233
import json
client = MongoDBClient233()

updata = Blueprint('updata', __name__)
@updata.route('/in/', methods=["POST"])
def up():
    data = request.get_data()
  
    data = json.loads(data)
    #print(type(data))
    user = client.info.find_one({"username":data["username"]})
    if user == None:
        print("11--------")
        client.info.insert(data)
        return jsonify({
            "error":"注册成功",
            "success":1
        })
    else:
        print("22---------")
    
        return jsonify({
            "error":"用户已注册",
            "success":0
        })


    

    