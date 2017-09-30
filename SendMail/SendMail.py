# -*- coding: UTF-8 -*-
import smtplib
import datetime
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendMail:
    def __init__(self, head=u'', body=u''):
        self.head = head
        self.body = body
        self.sendmailattach()

    def sendmailattach(self):
        msg = MIMEMultipart()
        # att = MIMEText(open(u'D:\cncepgf\workspace\PycharmProjects\my\\2017-07-02.xls', u'rb').read(), u'base64',
        #  u'utf-8')
        # att[u"Content-Type"] = u'application/octet-stream'
        # att[u"Content-Disposition"] = u'attachment; filename="' + self.filename.encode(u"gb2312") + u'"'
        # msg.attach(att)

        msg[u'to'] = u'@.com'
        msg[u'from'] = u'@.com'
        msg[u'cc'] = u'@.com'
        msg[u'subject'] = Header(self.head + u'(' + str(datetime.date.today()) + u')', u'utf-8')

        msg.attach(MIMEText(self.body.encode(u"utf-8"), u'plain'))

        server = smtplib.SMTP(u'smtp.exmail.qq.com', 25)
        server.login(u"@.com", u"")
        msg_text = msg.as_string()
        server.sendmail(msg[u'from'], msg[u'to'].split(u" ") + msg[u'cc'].split(u" "), msg_text)

if __name__ == u"__main__":
    SendMail(u'head', u'body')
