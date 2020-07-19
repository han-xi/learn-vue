from flask import jsonify, Blueprint,request
from mongoClient import MongoDBClient233
import json
client = MongoDBClient233()

loaddata = Blueprint('loaddata', __name__)
@loaddata.route('/loaddata', methods=["POST"])

def loadData():
    data = request.get_data()
    data = json.loads(data)
    userdata = client.info.find_one({"username":data['username']})
    if userdata == None:
    
        return jsonify({
            'error': "user not found.",
        }), 404
    else:
        if data['password'] == userdata["password"]:
            del userdata["_id"]

            return jsonify(userdata)
        else:
            return jsonify({
            'error': "密码错误.",
             }), 502
        # pa=[]
        # del userdata["_id"] 
        # for i in userdata:
        #    del i["_id"]
        #    pa.append(i) 
            
        # return jsonify(pa)