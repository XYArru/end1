import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

class confirmEmail():
    def __init__(self,receiver,userName):
        smtpserver = 'smtp.qq.com'
        username = '2898078974@qq.com'#发送方邮件地址
        password = 'vpfdjrjajiztdhcb' #授权码
        sender = username

        subject = '注册验证邮件，请勿回复'
        subject = Header(subject, 'utf-8').encode()

        # 构造邮件对象MIMEMultipart对象
        # 主题，发件人，收件人等显示在邮件页面上的。
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = 'Mr.Van'
        msg['To'] = receiver

        url = "127.0.0.1:8000/'%s'"%userName
        # 构造文字内容
        text = "Hi man!\n这是你的登录URL：" + url
        text_plain = MIMEText(text, 'plain', 'utf-8')
        msg.attach(text_plain)

        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        # 用set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息。
        # smtp.set_debuglevel(1)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()