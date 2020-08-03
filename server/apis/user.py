from flask import jsonify,g, Blueprint,request,session,redirect,Response,escape,make_response
import json
from datetime import datetime
import sys
sys.path.append('../')
from server.mongoClient import MongoDBClient233
from server.functions import md5value,genRandomString,send_email,validateEmail,validatePassword
from server.getsecertinfo import secert
import re
import os

secert_info=secert()
client = MongoDBClient233()
user = Blueprint('/user', __name__)

@user.route('/login', methods=["POST"])
def check_login():
    try:
        userinfo = request.get_json(force=True)
    except:
        return jsonify(None),400
    if  validateEmail(userinfo.get('username'))==False:
        return jsonify(None), 400
    if  validatePassword(userinfo.get('password'))==False:
        return jsonify(None), 400
    try: 
        db_userinfo = client.info.find_one({"username":userinfo["username"]})
    except:
        return jsonify(None), 500
    else:
        if db_userinfo is None:
            return jsonify({
                'error': "未发现用户",
            }), 404
        else:
            if md5value(db_userinfo["salt"]+userinfo['password'])== db_userinfo["password"]:
                session['user_id']=userinfo["username"]
                g.username=userinfo["username"]
                session.permanent = True
                client.info.update({"username":userinfo["username"]},{"$set":{"islogin":True}})
                return jsonify(None)
            else:
                return jsonify({
                'error': "密码错误",
                }), 400

@user.route('/register', methods=["POST"])
def check_register():
    try:
        postuserinfo = request.get_json(force=True)
    except:
        return jsonify(None),400
    if  validateEmail(postuserinfo.get('username'))==False:
        return jsonify(None), 400
    if send_email(str(postuserinfo['username']),client,'register'):#调用发送邮件逻辑部件
        return jsonify(None)#发送成功
    else:
        return jsonify(None),500

@user.route('/forget', methods=["POST"])
def check_forget():
    try:
        postuserinfo = request.get_json(force=True)
    except:
        return jsonify(None),400
    if  validateEmail(postuserinfo.get('username'))==False:
        return jsonify(None), 400
    if send_email(postuserinfo['username'],client,'forget'):#调用发送邮件逻辑部件
        return jsonify(None)#发送成功
    else:
        return jsonify(None),500

@user.route('/changepassword', methods=["POST"])
def update_password():
    try:    
        postuserinfo = request.get_json(force=True)
    except:
        return jsonify(None),400
    cookie=request.cookies
    #获取cookie
    if  validatePassword(postuserinfo.get('password'))==False:
        return jsonify(None), 400
    try:
        code=cookie.get('code')
        if isinstance(code,str)==False:
            return jsonify(None),400
        send_type=cookie.get('send_type')
        if isinstance(send_type,str)==False:
            return jsonify(None),400
    except AttributeError:
        return jsonify(None), 400
    if cookie['send_type']=='register':
        #检测邮件链接是否点击，如果已点击就返回错误，未点击就修改标志，检验是否注册，注册则取出用户名和密码插入数据库返回状态
        try:
            mail_info=client.mail.find_one({'type':cookie['send_type'],'code':code,'isactive':False})
        except:
            return jsonify(None),500
        if mail_info is not None:#链接是否有效
            try:
                user=client.info.find_one({'username':mail_info['username']})
            except:
                return jsonify(None),500
            if user is not None:#用户已注册
                try:
                    client.mail.update_one({'type':cookie['send_type'],'code':code,'isactive':False},{"$set":{'isactive':True}})
                except:
                    return jsonify(None),500
                return jsonify({"error":"用户已注册"}),400
            else:#用户未注册，进行注册同时修改链接
                salt=genRandomString()
                md5password=md5value(salt+postuserinfo['password'])
                nowtime = datetime.now() #获得当前时间
                try:
                    client.mail.update_one({'type':cookie['send_type'],'code':code,'isactive':False},{"$set":{'isactive':True}})
                    client.info.insert_one({
                        "username":mail_info['username'],
                        "password":md5password,
                        "registerdate":nowtime,
                        "salt":salt,
                        "islogin":False
                    })
                except:
                    return jsonify(None),500
                else:
                    return jsonify(None)
        else:
            return jsonify({"error":"code error"}),400
    elif cookie['send_type']=='forget':
        #检测邮件链接是否点击，如果已点击就返回错误，未点击就修改标志，检验是否注册，未注册则取出密码插入数据库返回状态
        try:
            mail_info=client.mail.find_one({'type':cookie['send_type'],'code':code,'isactive':False})
        except:
            return jsonify(None),500
        if mail_info is not None:#链接是否有效
            try:
                user=client.info.find_one({'username':mail_info['username']})
            except:
                return jsonify(None),500
            if user is None:#用户未注册取消链接
                try:
                    client.mail.update_one({'type':cookie['send_type'],'code':code,'isactive':False},{"$set":{'isactive':True}})
                except:
                    return jsonify(None),500
                return jsonify({"error":"用户未注册"}),404
            else:#用户未注册，进行注册同时修改链接
                salt=genRandomString()
                md5password=md5value(salt+postuserinfo['password'])
                try:
                    client.mail.update_one({'type':cookie['send_type'],'code':code,'isactive':False},{"$set":{'isactive':True}})
                    client.info.update({"username":mail_info["username"]},{"$set":{"password":md5password,'salt':salt}})
                except:
                    return jsonify(None),500
                else:
                    return jsonify(None)
        else:
            return jsonify(None),400

    # try:
    #     user = client.info.find_one({"username":postuserinfo["username"]})
    #     mail =client.mail.find_one({"tomail":postuserinfo["username"]})
    # except:
    #      return jsonify(None),500
    # else:
    #     nowtime = datetime.now() #获得当前时间
    #     if mail is None:#没有点击验证码的情况使得初始为空
    #         return jsonify({
    #             "error":"请点击发送按钮进行发送"
    #         }),501
    #     elif (nowtime-mail["maildate"]).seconds >= 600: #验证码超时十分钟
    #         return jsonify({
    #             "error":"验证码超时"
    #         }),501
    #     elif postuserinfo["smscode"]!=mail["code"]:
    #         return jsonify({
    #             "error":"验证码不正确"
    #         }),501
    #     if user is None:
    #         salt=genRandomString()
    #         md5password=md5value(salt+postuserinfo["password"])
    #         try:
    #             client.info.insert_one({
    #                 "username":postuserinfo["username"],
    #                 "password":md5password,
    #                 "registerdate":nowtime,
    #                 "salt":salt,
    #                 "islogin":False
    #             })
    #         except:
    #             return jsonify(None),500#数据库连接失败用500表示
    #         else:
    #             return jsonify(None)
    #     else:
    #         return jsonify({
    #             "error":"用户已注册",
    #         }),400

@user.route('/setpassword', methods=["POST"])
def set_password():
    postdata = request.get_json(force=True)
    if  validatePassword(postdata.get('password'))==False:
        return jsonify(None), 400
    password=postdata.get('password')
    try:
        user = client.info.find_one({"username":g.username})
    except:
         return jsonify(None),500#数据库连接失败用500表示   
    else: 
        if user is not None:
            salt=user["salt"]   
            md5password=md5value(salt+postdata["password"])
            try: 
                client.info.update({"username":g.username},{"$set":{"password":md5password}})
            except:
                return jsonify(None),500#数据库连接失败用500表示
            else:
                return jsonify(None)
        else:
            return jsonify({
                "error":"用户未注册",  
            }),404

@user.route('/logout', methods=["POST"])
def logout():
    if g.username is None:
        return jsonify(""),400
    try:
        client.info.update({"username":g.username},{"$set":{"islogin":False}})
    except:
        return jsonify(None),500
    else:
        session.clear()
        return jsonify(None)

@user.route('/active',methods=['GET','POST'])
def active():
    url=request.url
    url_info=re.search(r'.*code=(?P<active_code>.*).*&send_type=(?P<send_type>.*).*$',url)
    try:
        code=url_info.group('active_code')
        send_type=url_info.group('send_type')
    except AttributeError :
        response = make_response(
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
        "<title> ERROR</title>\n"
        "<h1>REQUEST ERROR</h1>\n"
        "<p>激活码格式错误</p> ")
        return response
    else:
        #检测用户是否存在
        try:
            mail=client.mail.find_one({"type":send_type,"code":code,'isactive':False})
        except:
            response = make_response(
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
                "<title> ERROR</title>\n"
                "<h1>500 ERROR</h1>\n"
                "<p>数据库连接失败</p> ")
            return response
        
        else:
            if mail is not None :
                response = make_response(
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
                "<title>Redirecting...</title>\n"
                "<h1>Redirecting...</h1>\n"
                "<p>You should be redirected automatically to target URL: "
                '<a href="%s">%s</a>.  If not click the link.'
                % (escape("https://www.baidu.com"),
                escape("https://www.baidu.com")), 302)
                response.set_cookie('code',code,domain='127.0.0.1')
                response.set_cookie('send_type',send_type,domain='127.0.0.1')
                response.location = escape('http://127.0.0.1:8080/#/PersonalCenterSetPassword')
                return response
            else:
                response = make_response(
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
                "<title> ERROR</title>\n"
                "<h1>REQUEST ERROR</h1>\n"
                "<p>激活码错误</p> ")
                return response
                
        