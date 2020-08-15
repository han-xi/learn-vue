from flask import jsonify,g, Blueprint,request,session,redirect,Response,escape,make_response,abort
import json
from datetime import datetime,timedelta
import sys
sys.path.append('../')
from server.mongoClient import MongoDBClient233
from server.functions import md5value,genRandomString,send_email,validateEmail,validatePassword,create_token,verify_token
from server.getsecertinfo import secert
import re
import os
from functools import wraps
#检验用户是否登录
def login_required(*role):
    def wrapper(func):
        def inner(*args, **kwargs):
            cookie=request.cookies
            if isinstance(cookie.get('token'),str) ==False:#token没有或者格式不对
                return jsonify(None),400
            token=verify_token(cookie['token'],*role)#是*role
            print(token)
            if  token==1:
                return jsonify({"error":"无权限"}),403
            elif token==2:
                return jsonify({"error":"登录失效"}),401
        
            return func(*args, **kwargs)
        return inner    
    return wrapper
    

secert_info=secert()
client = MongoDBClient233()

user = Blueprint('/user', __name__)
@user.route('/login', methods=["POST"])
def check_login():
    try:
        userinfo = request.get_json(force=True)
    except:
        #abort(400)
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
                #session['user_id']=userinfo["username"]
                g.username=userinfo["username"]
                if db_userinfo['level']=='vip':#根据权限生成token
                    #token=get_token(userinfo['username'],1)
                    token=create_token(db_userinfo['username'],'vip')
                elif db_userinfo['level']=='svip':
                    token=create_token(userinfo['username'],'svip')
                    g.levelendtime=userinfo['levelendtime']
                #session.permanent = True
                #client.info.update({"username":userinfo["username"]},{"$set":{'token':token,"tokenlifetime":datetime.now(),"islogin":True}})
                client.info.update({"username":userinfo["username"]},{"$set":{"islogin":True}})
                g.token=token
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
    if send_email(postuserinfo['username'],client,'register'):#调用发送邮件逻辑部件
        return jsonify({"send_mail":secert_info.mail['send_mail'],"send_time":secert_info.mail['send_time']})#发送成功
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
        return jsonify({"send_mail":secert_info.mail['send_mail'],"send_time":secert_info.mail['send_time']})#发送成功
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
                        "islogin":False,
                        "level":'vip',
                        "levellifetime":nowtime
                    })
                except:
                    return jsonify(None),500
                else:
                    return jsonify(None)
        else:
            return jsonify({"error":"激活码失效"}),400
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
            return jsonify({"error":"激活码失效"}),400

@user.route('/setpassword', methods=["POST"])
@login_required("admin",'svip','vip')
def set_password():
    try:#检验传过来的数据格式
        postdata = request.get_json(force=True)
    except:
        return jsonify(None), 400
    if  validatePassword(postdata.get('oldpassword'))==False:
        return jsonify(None), 400
    if  validatePassword(postdata.get('newpassword'))==False:
        return jsonify(None), 400
    cookie=request.cookies
    if isinstance(cookie.get('token'),str) ==False:#token没有或者格式不对
        return jsonify(None),400
    token=verify_token(cookie['token'],"admin","vip","svip") 
    try:#根据token查看用户
        user = client.info.find_one({"username":token['username'],'islogin':True})
    except:
        return jsonify(None),500#数据库连接失败用500表示   
    else: 
        if user is not None:
            salt=user["salt"]  
            if  md5value(salt+postdata["oldpassword"])!=user["password"]:#提交的旧密码不对
                return jsonify({"error":"密码错误"}),400
            md5password=md5value(salt+postdata["newpassword"])
            try:#更新密码 
                client.info.update({"username":token['username'],'islogin':True},{"$set":{"password":md5password}})
            except:
                return jsonify(None),500#数据库连接失败用500表示
            else:
                return jsonify(None)
        else:
            return jsonify({
                "error":"用户未注册",  
            }),404

@user.route('/logout', methods=["POST"])
#@login_required("admin","vip","svip")
def logout():
    cookie=request.cookies
    if isinstance(cookie.get('token'),str) ==False:#token没有或者格式不对
        return jsonify(None),400
    token=verify_token(cookie['token'],"admin","vip","svip")  
    try: 
        client.info.update({"username":token['username'],'islogin':True},{"$set":{"islogin":False}})
    except:
        return jsonify(None),500
    else:
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
                if (datetime.now()-mail['send_time']).seconds<secert_info.mail['send_time']*24*3600:
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
                    client.mail.update_one({'type':send_type,'code':code,'isactive':False},{"$set":{'isactive':True}})
                    response = make_response(
                    '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
                    "<title> ERROR</title>\n"
                    "<h1>REQUEST ERROR</h1>\n"
                    "<p>激活码超时</p> ")
                    return response     
            else:
                response = make_response(
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
                "<title> ERROR</title>\n"
                "<h1>REQUEST ERROR</h1>\n"
                "<p>激活码错误</p> ")
                return response
                
@user.route('/level/grant',methods=['POST'])
def grant():
    level=request.get_json(force=True)
    cookie=request.cookies
    try:
        user=client.info.find_one({"token":cookie['token']})
    except:
        return jsonify(None),500
    set_grant(user["username"],level)

def set_grant(username,level):
    if level==1:#月
        endtime=datetime.now()+timedelta(days=31)
    elif level==2:#季
        endtime=datetime.now()+timedelta(days=91)
    elif level==3:#年
        endtime=datetime.now()+timedelta(days=365)
    else:
        return False
    try:
        token=create_token(username,'svip')
        g.levelendtime=endtime
        g.token=token
        client.info.update({"username":username},{"$set",{"token":token,"level":2,"levelendtime":endtime}})
    except:
        return False
    return True

    
    