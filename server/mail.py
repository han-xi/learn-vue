from flask import jsonify, Blueprint,request
from mongoClient import MongoDBClient233
import json
# smtplib 用于邮件的发信动作
import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
# 用于构建邮件头
client = MongoDBClient233()

mail = Blueprint('mail', __name__)
@mail.route('/mail', methods=["POST"])
def sendmail():
    data = request.get_data()
    data = json.loads(data)
    #print(type(data))
    try:
        mails = client.mail.find_one({"tomail":data["tomail"]})
        if mails == None:
            client.mail.insert(data)
        else:
            client.mail.remove({"tomail":data["tomail"]})
            client.mail.insert(data)
    except:
        return jsonify({
            "error":"数据库连接失败"
        }),700    
    else:
        # 发信方的信息：发信邮箱，QQ 邮箱授权码
        from_addr = '1179865214@qq.com'
        password = 'rpvcmpolnvdngfhd'
    
        # 收信方邮箱
        to_addr = data["tomail"]
    
        # 发信服务器
        smtp_server = 'smtp.qq.com'
    
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText('您的激活码是'+data["code"]+'在十分钟之内有效','plain','utf-8')
    
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
                "error":"发送邮件失败"
            }),700
        else:
            return jsonify({
                "success":"发送成功" 
            })

    # @mail.route('/mail', methods=["GET"])
    # def getMail():
    #     data = client.mail.find()