# -*- coding: UTF-8 -*-
__author__ = 'Administrator'

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib, datetime


class SendMail():
    def __init__(self, head='', body=''):
        self.head = head
        self.body = body
        self.SendMailAttach()

    def SendMailAttach(self):
        msg = MIMEMultipart()
        # att = MIMEText(open(u'D:\cncepgf\workspace\PycharmProjects\my\\2017-07-02.xls', 'rb').read(), 'base64', 'utf-8')
        # att["Content-Type"] = 'application/octet-stream'
        # att["Content-Disposition"] = 'attachment; filename="chongfu.xls"'
        # msg.attach(att)

        msg['to'] = '@.com'
        msg['from'] = '@.com'
        msg['CC'] = '@.com'
        msg['subject'] = Header(self.head + '(' + str(datetime.date.today()) + ')', 'utf-8')

        msg.attach(MIMEText(self.body, 'plain'))

        server = smtplib.SMTP('smtp.exmail.qq.com', 25)
        server.login("@.com", "")
        msg_text=msg.as_string()
        server.sendmail(msg['from'], msg['to'],msg_text)

if __name__ == "__main__":
    SendMail('head', 'body')





