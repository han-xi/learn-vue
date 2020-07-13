from flask import jsonify, Blueprint
from mongoClient import MongoDBClient233
client = MongoDBClient233()

loaddata = Blueprint('loaddata', __name__)
@loaddata.route('/<username>/<password>')
def loadData(username,password):
    userdata = client.info.find_one({"username":username})
    if userdata == None:
    
        return jsonify({
            'error': "user not found.",
        }), 404
    else:
        if password == userdata["password"]:
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