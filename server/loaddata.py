from flask import jsonify, Blueprint,request,session
from mongoClient import MongoDBClient233
import json
client = MongoDBClient233()

loaddata = Blueprint('loaddata', __name__)
@loaddata.route('/loaddata', methods=["POST"])

def loadData():
    data = request.get_data()
    data = json.loads(data)
    try: 
        userdata = client.info.find_one({"username":data['username']})
    except:
        #print("122222")
        return jsonify({
        }), 500
    else:
        if userdata == None:
            return jsonify({
                'error': "未发现用户.",
            }), 401
        else:
            if data['password'] == userdata["password"]:
                session['user_id']=data['username']
                session.permanent = True
                del userdata["_id"]
                temp={}
                temp.update({"errCode":3})
                #temp.update({"token":userdata["token"]})
                return jsonify(temp)
            else:
                return jsonify({
                'error': "密码错误.",
                }), 401