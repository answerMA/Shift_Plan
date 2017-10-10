#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/1/2017 6:45 PM
# @Author  : Ruiming_Ma
# @Site    : 
# @File    : entry.py
# @Software: PyCharm Community Edition

import ShiftPlan
from apscheduler.schedulers.background import BlockingScheduler
import logging
import WeChatSender


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./logs/app_out_entry.log',
                    filemode='w')


def CheckWebFile():
    logging.info('\tStarting')
    status = ShiftPlan.shiftplan()
    logging.info('\tDone')
    if not status:
        logging.info('No updates of Shiftplan')
    else:
        WeChatSender.send_shiftplan()



def CheckLocalFile():
    pass


def main():
    WeChatSender.login_in()
    scheduler = BlockingScheduler()
    scheduler.add_job(func=CheckWebFile, trigger='interval', minutes=30)
    try:
        scheduler.start()
    except:
        logging.warning('Scheduler Error\n')
        scheduler.shutdown()


main()
