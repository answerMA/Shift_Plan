#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/26/2017 10:54 AM
# @Author  : Ruiming_Ma
# @Site    : 
# @File    : ShiftPlan.py
# @Software: PyCharm Community Edition


from selenium import webdriver
from pyquery import PyQuery as pq
from urllib.parse import urlencode
import time
import os
import json
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./logs/app_out_ShiftPlan.log',
                    filemode='w')


def getHTML():
    base_url = 'http://workit.nnitcorp.com/Departments/086-0961/Middleware/Shared%20Documents/Forms/AllItems.aspx?'
    data = {
        'RootFolder': '/Departments/086-0961/Middleware/Shared Documents/Teamet',
        'FolderCTID': '0x012000AB0EFC565D555D4D91F529154D3A4370',
        'View': '{1E7886D2-76B5-4C07-928B-066391081D2C}'
    }
    url = base_url + urlencode(data, encoding='utf-8')

    browser = webdriver.PhantomJS()
    browser.get(url)
    html = browser.page_source
    browser.quit()
    return html


def parseHTML(page):
    name_list = []
    time_list = []
    dict_list = []

    doc = pq(page)
    names = doc.find('.ms-subtleLink')
    for name in names.items():
        name_list.append(name.text())

    times = doc.find('.ms-cellstyle.ms-vb2 span')
    for time in times.items():
        time_list.append(time.attr('title'))

    dicts = doc.find('.ms-vb.itx a')
    for dict in dicts.items():
        dict_list.append(dict.text())

    if len(name_list) == len(time_list) == len(dict_list):
        for i in range(len(name_list)):
            yield {
                'name': dict_list[i],
                'time': time_list[i],
                'author': name_list[i]
            }
    else:
        logging.warning("\tread page error\n")


def getOneDoc(items, name):
    names = []
    for item in items:
        names.append(item['name'])
        if item['name'] == name:
            doc = item
    if name not in names:
        logging.warning('\tDocument Not Found, Please Confirm the File Name\n')
        return None
    else:
        return doc


def Write2Json(file, path):
    data = [file]
    if file:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, indent=2))
        logging.info('\tWrote into File Successully')
    else:
        logging.warning('\tNot Got Any Data From SharePoint, Please Check the URL!')


def ReadFromJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        file = f.read()
    data = json.loads(file)
    return data.pop()


def CompareFiles(originalFile):
    fileName = 'shiftplan.log'
    filePath = r'.\configs'
    totalPath = filePath + '\\' + fileName

    if not os.path.isfile(totalPath):
        if not os.path.exists(filePath):
            os.mkdir(filePath)
        logging.info('\tFile not Existed, Creating Now')
        Write2Json(originalFile, totalPath)
        return True
    else:
        data = ReadFromJson(totalPath)

    time_1 = originalFile['time']
    time_2 = data['time']

    if time_1 == time_2:
        return False
    else:
        logging.info('\tShiftPlan is Updating')
        Write2Json(originalFile, totalPath)
        return True


def Download():  # 使用Chromedriver 2.29 version
    file = r'.\files\Shiftplan24_7_v1.xls'
    if os.path.isfile(file):
        os.remove(file)
        logging.info('The Previous File Has Been Deleted')

    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': r'C:\Users\ruim.NNITCORP\Desktop\Middleware\Python\ShiftPlan\files'}
    options.add_experimental_option('prefs', prefs)
    # options.add_argument('--headless') #使用于Chrome 59&60 的Headless模式
    # options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=r'C:\Temp\jdk1.8.0\bin\chromedriver.exe', chrome_options=options)
    driver.get(
        'http://workit.nnitcorp.com/Departments/086-0961/Middleware/Shared%20Documents/Teamet/Shiftplan24_7_v1.xls')
    logging.info('\tThe File is downloading, please wait for a while')
    time.sleep(2)
    driver.quit()
    logging.info('\tDownload Completed!')


def recordModifyTime():
    file_path = r'.\configs'
    shiftplan_path = file_path + '\\' + 'shiftplan.log'
    time_record_path = file_path + '\\' + 'time_record.log'
    if os.path.exists(file_path):
        if os.path.isfile(shiftplan_path):
            timestamp = time.ctime(os.path.getmtime(shiftplan_path))
            with open(time_record_path, 'w') as f:
                f.write(timestamp)
        else:
            logging.warning('shiftplan in not existing in the configs folder')

    else:
        logging.warning('confid folder is not existing, can not create time_record.log')


def checkModifyTime():
    file_path = r'.\configs'
    shiftplan_path = file_path + '\\' + 'shiftplan.log'
    tim_record_path = file_path + '\\'+ 'time_record.log'
    if os.path.isfile(tim_record_path):
        with open(tim_record_path,'r') as f:
            read_time = f.read()
        timestample = time.ctime(os.path.getmtime(shiftplan_path))
        if timestample != read_time:
            pass




def shiftplan():
    html = getHTML()
    docs = parseHTML(html)
    item = getOneDoc(docs, 'Shiftplan24_7_v1.xls')
    if CompareFiles(item):
        Download(downloadPath)
        return True
    else:
        logging.info('\tNo Updates of ShiftPlan')
        return False
