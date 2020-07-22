from flask import jsonify, Blueprint,request,session
from mongoClient import MongoDBClient233
import json
client = MongoDBClient233()

loaddata = Blueprint('loaddata', __name__)
@loaddata.route('/loaddata', methods=["POST"])

def loadData():
    data = request.get_data()
    head=str(request.headers)
    print(head)
    #print(request.getCookies())

    print(str(request.cookies))
    #print(str(request.cookies))
    print("--------------")
    #print (data["params"])
    print(data)
    data = json.loads(data)
    print(data)
    try: 
        userdata = client.info.find_one({"username":data['username']})
    except:
        return jsonify({
            'error': "数据库连接失败",
        }), 311
    else:
        if userdata == None:
            return jsonify({
                'error': "user not found.",
            }), 311
        else:
            if data['password'] == userdata["password"]:
                session['user_id']=data['username']
                session.permanent = True
                del userdata["_id"]
                temp={}
                temp.update({"errCode":2})
                temp.update({"token":userdata["token"]})
                return jsonify(temp)
            else:
                return jsonify({
                'error': "密码错误.",
                }), 311
            # pa=[]
            # del userdata["_id"] 
            # for i in userdata:
            #    del i["_id"]
            #    pa.append(i) 
                
            # return jsonify(pa)