#!/usr/bin/env python
#/usr/bin/python3
#!#/usr/bin/python3
#-*- coding:utf-8 -*-
# web crawler for artstation
# author : wangzhen <wangzhenjjcn@gmail.com> since 2019-03-15


import os
import re
import sys
import time
import lxml
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
 
def main():
    dir_=""
    username=""
    password=""
    username=input("输入九州通用户名：")
    password=input("输入九州通密码：")
    dir_=input("请输入数据存储目录:")
    if dir_=="" or  username=="" or password=="":
        return
    filename=dir_+"/九州通医保药品信息.csv"
    if os.path.exists(dir_):
        print(dir_)
    else:
        os.makedirs(dir_, exist_ok=True)
    if not os.path.exists(dir_):
        return
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options,executable_path='./chrome/chrome.exe')
 
    # browser = webdriver.Chrome()
    browser.get("http://fw9.yyjzt.com/user/login.htm")
    browser.find_element_by_id("jzt_username").send_keys(username) 
    browser.find_element_by_id("jzt_password").send_keys(password) 
    browser.find_element_by_xpath('//*[@id="login_form_id"]/div[4]/button').click()
    time.sleep(2)
    browser.get("http://fw9.yyjzt.com/market/salefair/activityinfo/index.htm?pageId=4848")
    time.sleep(2)
    for i in range(1,15):
        browser.execute_script("window.scrollBy(0,"+str(i*5000)+")")
        time.sleep(1)  
    uls = browser.find_elements_by_xpath('//*[@id="Z129904313993961540"]/div/ul/li')
    datas=[]
    for li in uls:
        data={}
        price=0
        name=""
        guige=""
        changjia=""
        qiangguang=""
        lis=str(li.text).split( )
        if '抢光了' in li.text :
            qiangguang="抢光了"
            price=lis[1].replace("¥","")
            name=lis[2]
            guige=lis[3]
            changjia=lis[4]
        else:
            qiangguang="有"
            price=lis[0].replace("¥","")
            name=lis[1]
            guige=lis[2]
            changjia=lis[3]
        data['price']=price.replace("¥","")
        data['name']=name
        data['guige']=guige
        data['changjia']=changjia
        data['qiangguang']=qiangguang
        print(data)
        datas.append(data)
 
    with open(filename, 'w') as f:
        f.write("序列,名称,厂家,规格,价格,是否有货\n")
        num=0
        for data in datas:
            num+=1
            f.write(str(num)+','+data['name']+','+data['changjia']+','+data['guige']+','+data['price']+','+data['qiangguang']+'\n')
 
    f.close()


    # browser = webdriver.Chrome()
    # browser.get(" https://www.artstation.com/users/beeple/projects.json?page=1")
    # page=browser.page_source
    # html = BeautifulSoup(browser.page_source, "lxml")
    # pre = html.findAll('pre')
    # print(pre[0].contents[0])
    # j = json.loads(pre[0].contents[0])
    # print(len(j['data']))
    # cookies=browser.get_cookies()
if __name__ == '__main__':
    main()
