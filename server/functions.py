import hashlib
import random,string
from mongoClient import MongoDBClient233
import json
# smtplib 用于邮件的发信动作
import smtplib
from email.mime.text import MIMEText
from flask import jsonify, Blueprint,request,current_app
# email 用于构建邮件内容
from email.header import Header
from datetime import datetime
from getsecertinfo import secert
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def validateEmail(s):
    temp="^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
    #temp ='^(?=.*[(a-z)|(A-Z)])(?=.*\d)[^]{6,16}$'
    try:
        if re.match(temp,s)!=None:
            return True
        else :
            return False
    except:
        return False
def validatePassword(s):
    if isinstance(s,str):
        return True
    else:   
        return False

def md5value(s):
    md5 = hashlib.md5()
    md5.update(s.encode())
    return md5.hexdigest()

def genRandomString(slen=10):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))

def create_token(user_name, role_list):
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=current_app.config["TOKEN_EXPIRATION"])
    # 接收用户id转换与编码
    token = None
    try:
        token = s.dumps({"username": user_name, "role": role_list}).decode("ascii")
    except Exception as e:
        current_app.logger.error("获取token失败:{}".format(e))
    return token
    
def verify_token(token,*role):#是tuple类型role否则list(role)会出错
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        # 转换为字典
        data = s.loads(token)
        token_role=data.get('role').split(' ')
        if token_role:
            # 获取token中的权限列表如果在参数列表中则表示有权限，否则就表示没有权限
            #user_role = current_app.config['ROLE_LIST']
            result = [x for x in list(role) if x in token_role]
            if not result:
                return 1
            else:
                return data
    except Exception as e:
        return 2
def send_email(mail_name,client,send_type):
    server_info=secert()
    if send_type == 'forget':
        random_code = genRandomString(8)
    else:
        random_code = genRandomString(6)
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = server_info.mail['send_mail']
    password = server_info.mail['mail_password']
    # 收信方邮箱
    to_addr = mail_name
    # 发信服务器
    smtp_server = server_info.mail['smtp_server']
    #端口
    port=server_info.mail['port']
    
    if send_type=='register':
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText('<h1 style="color:red；font-size:100px">请点击下面的链接激活您的账号：<a href="http://127.0.0.1:9004/user/active?code={code}&send_type={send_type}">http://127.0.0.1:9004/user/active?code={code}&send_type={send_type}</a></h1>'.format(code=random_code,send_type=send_type),'html','utf-8')
        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header('专利系统注册激活链接')
    elif send_type=='forget':
        msg = MIMEText('<h1 style="color:red；font-size:100px">请点击下面的链接重置您的账号：<a href="http://127.0.0.1:9004/user/active?code={code}&send_type={send_type}">http://127.0.0.1:9004/user/active?code={code}&send_type={send_type}</a></h1>'.format(code=random_code,send_type=send_type),'html','utf-8')
        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header('专利系统密码重置链接')
    else:
        return False
    try:
        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server,port)
        # 登录发信邮箱
        server.login(from_addr, password)
        # 发送邮件
        server.sendmail(from_addr, to_addr, msg.as_string())
        # 关闭服务器
        server.quit() 
    except:
        return False
    else:

        try:
            client.mail.insert_one({'type':send_type,'username':mail_name,'code':random_code,'isactive':False,'send_time':datetime.now()})
        except:
            return False
        return True

