from flask import jsonify, Blueprint,request
from mongoClient import MongoDBClient233
import json
client = MongoDBClient233()

updata = Blueprint('updata', __name__)
@updata.route('/updata', methods=["POST"])
def up():
    data = request.get_data()
    data = json.loads(data)
    try:
        user = client.info.find_one({"username":data["username"]})
    except:
         return jsonify({#数据库连接失败用500表示
            }),500
    else:
        if user == None:
            try:
                client.info.insert(data)
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