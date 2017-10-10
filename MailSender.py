#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/1/2017 9:33 PM
# @Author  : Ruiming_Ma
# @Site    : 
# @File    : MailSender.py
# @Software: PyCharm Community Edition

#发送邮件需要占用1024以下的端口，比如SMTP占用的25等，这些端口的使用权需要管理员的权限，但是在目前来说做不到，所以不能发送邮件

import email
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def sendEmail(authInfo, fromAdd, toAdd, subject):
    strFrom = fromAdd
    strTo = ','.join(toAdd)

    server = authInfo.get('server')
    user = authInfo.get('user')
    passwd = authInfo.get('password')

    if not(server and user and passwd):
        print('Login Info is not completely, please fill in')
        return None

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi=part message in MIMEformat.'

    path = r'C:\Users\ruim.NNITCORP\Desktop\Middleware\Python\ShiftPlan\QR.png'
    fp = open(path, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    smtp = smtplib.SMTP(server, '587')
    smtp.set_debuglevel(1)
    #smtp.connect(server)
    smtp.login(user, passwd)
    smtp.send_message(strFrom, strTo, msgRoot.as_string())
    smtp.quit()
    return None


def main():
    authInfo = {}
    authInfo['server'] = 'smtp.126.com'
    authInfo['user'] = 'answer_MA'
    authInfo['password'] = '*******'
    fromAdd = 'answer_MA@126.com'
    toAdd = 'ruim@nnit.com'
    subject = 'QR Code'
    sendEmail(authInfo, fromAdd, toAdd,subject)


main()