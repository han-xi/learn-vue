from flask import jsonify, Blueprint,request
from mongoClient import MongoDBClient233
import json
# smtplib 用于邮件的发信动作
import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
from datetime import datetime
import random,string
#

def genRandomString(slen=6):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))
# 用于构建邮件头
client = MongoDBClient233()

userMail = Blueprint('userMail', __name__)
@userMail.route('/userMail', methods=["POST"])
def send_mail():
    mail_name = request.get_data()
    mail_name = json.loads(mail_name)
    #print(type(data))
    random_code=genRandomString()
    try:
        db_mail = client.mail.find_one({"tomail":mail_name["tomail"]})
        now_time = datetime.now() #获得当前时间
        if db_mail == None:
            mail_info={}
            mail_info.update({"code":random_code})
            mail_info.update({"tomail":mail_name["tomail"]})
            mail_info.update({"maildate":now_time})
            client.mail.insert(mail_info)
        else:
            #更新时间和验证码
            client.mail.update({"tomail":mail_name["tomail"]},{"$set":{"maildate":now_time,"code":random_code}})
    except:
        return jsonify({
        }),500    
    else:
        # 发信方的信息：发信邮箱，QQ 邮箱授权码
        from_addr = '1179865214@qq.com'
        password = 'rpvcmpolnvdngfhd'
    
        # 收信方邮箱
        to_addr = mail_name["tomail"]
    
        # 发信服务器
        smtp_server = 'smtp.qq.com'
    
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText('您的激活码是'+random_code+'在十分钟之内有效','plain','utf-8')
    
        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header('python test')
        try:
            # 开启发信服务，这里使用的是加密传输
            server = smtplib.SMTP_SSL(smtp_server)
            server.connect(smtp_server,465)
            # 登录发信邮箱
            server.login(from_addr, password)
            # 发送邮件
            server.sendmail(from_addr, to_addr, msg.as_string())
            # 关闭服务器
            server.quit() 
        except:
            return jsonify({
                "error":"发送失败"
            }),510
        else:
            return jsonify({
               # "error":"发送成功" 

            })