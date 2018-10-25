#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
    @author:wangzhen
    @contact: zhen.wang@ontim.cn
    @file: Email.py
    @time: 2018-09-05
    @desc:
    """

# coding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import config


class Email:

    def __init__(self,subject,receiver,mail_msg):
        self.subject = subject
        self.receiver = receiver
        self.mail_msg = mail_msg

    def set_subject(self, subject):
        self.subject = subject

    def set_receiver(self, receiver):
        self.receiver = receiver

    def send_email(self):
        # 设置smtplib所需的参数
        # subject = self.subject
        # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
        # subject = '中文标题'
        msg = MIMEMultipart("mixed")
        # 构造邮件对象MIMEMultipart对象
        # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
        sender_tag = u"自动化Monkey测试系统"

        msg['Subject'] = Header(self.subject,'utf-8')
        msg['From'] = config.SEND_EMAIL_ADDR
        # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
        msg['To'] = ";".join(self.receiver)
        # msg['Date']='2012-3-16'



        # # 构造文字内容
        text = self.mail_msg
        text_plain = MIMEText(text, 'plain', 'utf-8')
        msg.attach(text_plain)

        # 构造图片链接
        # sendimagefile = open(r'testimage.png', 'rb').read()
        # image = MIMEImage(sendimagefile)
        # image.add_header('Content-ID', '<image1>')
        # image["Content-Disposition"] = 'attachment; filename="testimage.png"'
        # msg.attach(image)

        # 构造html
        # 发送正文中的图片:由于包含未被许可的信息，网易邮箱定义为垃圾邮件，报554 DT:SPM ：<p><img src="cid:image1"></p>
        # html = """
        # <html>
        #   <head></head>
        #   <body>
        #     <p>Hi!<br>
        #        How are you?<br>
        #        Here is the <a href="http://www.baidu.com">link</a> you wanted.<br>
        #     </p>
        #   </body>
        # </html>
        # """
        # text_html = MIMEText(html, 'html', 'utf-8')
        # text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'
        # msg.attach(text_html)

        # 构造附件
        sendfile = open(r'readme.txt', 'rb').read()
        text_att = MIMEText(sendfile, 'base64', 'utf-8')
        text_att["Content-Type"] = 'application/octet-stream'
        # 以下附件可以重命名成aaa.txt
        # text_att["Content-Disposition"] = 'attachment; filename="aaa.txt"'
        # 另一种实现方式
        text_att.add_header('Content-Disposition', 'attachment', filename='aaa.txt')
        # 以下中文测试不ok
        # text_att["Content-Disposition"] = u'attachment; filename="中文附件.txt"'.decode('utf-8')
        msg.attach(text_att)

        # 发送邮件
        try:
            smtp = smtplib.SMTP()
            smtp.connect(config.SMTP_SERVER)
            # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
            # smtp.set_debuglevel(1)
            smtp.login(config.SEND_EMAIL_ADDR, config.SEND_EMAIL_PWD)
            smtp.sendmail(config.SEND_EMAIL_ADDR, self.receiver, msg.as_string())
            smtp.quit()
            print "邮件发送成功"
        except smtplib.SMTPException:
            print "Error :无法发送邮件"

# if __name__ == '__main__':
#     email = Email("自动化Monkey测试报告",config.RECEIVE_EMAIL_ADDR,"MonkeyAutotest , No need to reply\nMonkey测试结果，不需回复此邮件")
#     email.send_email()