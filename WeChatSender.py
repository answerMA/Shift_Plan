#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/28/2017 8:55 AM
# @Author  : Ruiming_Ma
# @Site    : 
# @File    : WeChatSender.py
# @Software: PyCharm Community Edition



import itchat
import requests
import ShiftPlan
import logging
import AX
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./logs/app_out_WeChatSener.log',
                    filemode='w')

KEY = '2743113ce1c64cecba75232efd63c876'
PATH = r'.\configs\shiftplan.log'


def get_response(msg):  # 添加一个图灵机器人作为回答文本消息
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot'
    }

    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return


def get_shiftplan():  # 获取排班表更新细节
    data = ShiftPlan.ReadFromJson(PATH)
    return u'排班表由 {0} 在 {1} 更新'.format(data['author'], data['time'])


def log_out():
    send_Logouttext()
    itchat.logout()


@itchat.msg_register(itchat.content.TEXT)  # 使用装饰器注册该函数为接受到文本消息时使用的函数
def auto_send_message(msg):
    defaultReply = 'I received :' + msg['Text']
    reply = get_response(msg['Text'])
    if msg['Text'] == u'排班表':
        name = msg['FromUserName']
        str = get_shiftplan()
        itchat.send_file(fileDir=r'.\files\Shiftplan24_7_v1.xls', toUserName=name)
        return str
    elif msg['Text'] == 'EXIT!':
        log_out()
    elif msg['Text'] == 'AX':
        name = msg['FromUserName']
        AX_result = AX.respone_isFriday()
        itchat.send(AX_result, toUserName=name)
        AX_result = AX.response_isMonthDeadline()
        itchat.send(AX_result, toUserName=name)
    else:
        return reply or defaultReply


def get_contact():
    names = []
    friends = itchat.get_friends(update=True)
    for friend in friends:
        names.append(friend['UserName'])

    return names


def send_Logintext():
    names = get_contact()
    for name in names:
        itchat.send(u'小M已上线，请回复"排班表"查询最近班表', toUserName=name)
        logging.info(u'登录信息已群发')


def send_AX():
    names = get_contact()
    if AX.isFriday():
        for name in names:
            time.sleep(1)
            itchat.send(u'今天是礼拜五，请及时注 AX !', toUserName=name)
            logging.info('AX_Friday 已群发')
    elif AX.isMonthDeadline():
        for name in names:
            time.sleep(1)
            itchat.send(u'今天是月结日，请及时注 AX !', toUserName=name)
            logging.info('AX_Month_Deadline 已群发')


def send_shiftplan():
    names = get_contact()
    for name in names:
        itchat.send('@fil@\files\Shiftplan24_7_v1.xls', toUserName=name)
        itchat.send_file(fileDir=r'.\files\Shiftplan24_7_v1.xls', toUserName=name)
        details = get_shiftplan()
        itchat.send(details, toUserName=name)


def send_Logouttext():
    names = get_contact()
    for name in names:
        itchat.send(u'小M已下线，不再提供排班表查询以及聊天业务咯', toUserName=name)
        logging.info(u'登出信息已群发')


def login_in():
    # RUIM在itchat中的login文件将主动显示QR关闭，现在只是存文件而已
    # 由于本机器没有管理员权限，导致不能发送邮件，所以显示QR的功能又开启了 10/1/2017

    # path = r'C:\Users\ruim.NNITCORP\Desktop\Middleware\Python\ShiftPlan\QR.png'
    # itchat.auto_login(picDir=path, hotReload=True)
    itchat.auto_login(hotReload=False)
    send_Logintext()
    send_AX()
    itchat.run(blockThread=False)
