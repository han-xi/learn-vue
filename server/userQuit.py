from flask import jsonify, Blueprint,request,session


userQuit = Blueprint('userQuit', __name__)
@userQuit.route('/userQuit', methods=["GET"])
def del_session():
    session.clear()
    return jsonify({
    })