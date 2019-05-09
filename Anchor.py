#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AUTHOR:VRING
# DATETIME:2019\5\6 0006 10:24
# SOFTWARE:PyCharm

from Common.log import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import random
import threading
import requests
import numpy
options = webdriver.ChromeOptions()
prefs = {}
# 设置这两个参数就可以避免  是否保存密码提示框  的弹出
prefs["credentials_enable_service"] = False
prefs["profile.password_manager_enabled"] = False
options.add_experimental_option("prefs", prefs)
# #实例化一个启动参数对象
# chrome_options = options
# 测试数据存放路径以及文件  Error：非法参数
Testinfo = "E:\\Test_Maven_SSM\\shop_z.csv"
LoginUrl="https://www.zhiboshuju.com/login.ftl"

# 错误信息处理
def erro_log(e_error):
    error = []
    error.append(e_error)
    new_index = error[0]
    str_e = str(new_index)
    new_error = []
    new_error = str_e.split("(Session", 1)
    return new_error[0]

#  省市区选择
def choose(parent_ele):
    children_ele = parent_ele.find_elements_by_tag_name("a")
    ele_list = []
    for aop in children_ele:
        ele_list.append(aop.get_attribute("text"))
    #转换成数组
    item = numpy.array(ele_list)
    set_count = len(item)
    #   1--34
    chose_index = random.randint(1,set_count)
    return chose_index

# 超时设置
def out_time(driver,url,element_str,state):
    try:
        '''
         driver.set_page_load_timeout(10)
         隐式等待   driver.implicitly_wait(1)
         显示等待   在页面查找需要的元素是否有在指定时间内出现  如果在指定时间内出现  则通过  若超出指定时间  则抛出异常
        '''
        if 1 == state:
            #判断元素 是否可点击
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, element_str)))
        elif 2 == state:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.LINK_TEXT, element_str)))
        elif 3 == state:
            str_xpath  = str(element_str)
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,str_xpath)))
        req = requests.get(url)
        logger.info("当前页面响应总时长 ："+str(req.elapsed.total_seconds()*10))
    except Exception as e:
        logger.error("TimeOutException")
        driver.close()


def Fellow(line,Userinfo_reader):
    driver = webdriver.Chrome()
    driver.maximize_window()
    logger.info("开始测试账号："+line[0]+"  密码："+line[1])
    driver.get(LoginUrl)
    out_time(driver,LoginUrl,"user",1)
    try:
        # 商家
        # driver.find_element_by_xpath("/html/body/div[2]/div/div/h3/span[2]").click()
        #主播
        driver.find_element_by_xpath("/html/body/div[2]/div/div/h3/span[1]").click()
        user = driver.find_element_by_id("user")
        user.send_keys(line[0])
        passd = driver.find_element_by_id("pass")
        passd.send_keys(line[1])
        driver.find_element_by_xpath("/html/body/div[2]/div/div/form/button").click()
        time.sleep(2)
        req = requests.get(driver.current_url)
        out_time(driver,driver.current_url,line[0]+"(个人中心)",2)
        # logger.info("首页响应总时长 ：" + str(req.elapsed.total_seconds() * 10))
        # 个人中心
        person = driver.find_element_by_xpath("//*[@id='navbar']/ul[2]/li[3]/a")
        flag = person.is_displayed()
        if flag == True:
            logger.info("登录成功")
            # 首页弹出广告
            driver.find_element_by_xpath("/html/body/div[1]/div/i").click()
            person.click()
            logger.info("进入个人中心")
            # out_time(driver.current_url,"修改密码",2)
            #   商家
            # driver.find_element_by_link_text("帮助中心").click()
            # 主播

            driver.find_element_by_link_text("个人信息").click()
            driver.find_element_by_link_text("收样地址").click()
            iframe = driver.find_elements_by_tag_name('iframe')[0]
            # 切换到添加的iframe
            driver.switch_to.frame(iframe)
            #开始添加
            driver.find_element_by_xpath("//*[@id='addAddress']").click()
            add={
                "name":"严将",
                "phone":189009990099,
                "address":"xx街道xx号",
                "email":"0000000"
            }
            #  存入新地址
            shop_name = driver.find_element_by_xpath("//*[@id='contactor-form']/div/input")
            shop_name.click()
            shop_name.send_keys(add["name"])
            shop_phone = driver.find_element_by_xpath("//*[@id='form']/div[3]/div/input")
            shop_phone.click()
            shop_phone.send_keys(add["phone"])
            shop_address = driver.find_element_by_xpath("//*[@id='form']/div[5]/div/input")
            shop_address.click()
            shop_address.send_keys(add["address"])
            shop_email = driver.find_element_by_xpath("//*[@id='form']/div[6]/div/input")
            shop_email.click()
            shop_email.send_keys(add["email"])
            #   地址信息   //*[@id="form"]/div[4]/div
            # driver.find_element_by_xpath("//*[@id='form']/div[4]/div").click()
            # time.sleep(3)
            # #省
            # a_index = "//*[@id='form']/div[4]/div/div/div/div[2]/div[1]/dl/dd/a["
            # driver.find_element_by_link_text("城市").click()
            # time.sleep(2)
            # parent_shen = driver.find_element_by_xpath("//*[@id='form']/div[4]/div/div/div/div[2]/div[1]/dl/dd")
            # key_shen = choose(parent_shen)
            # driver.find_element_by_xpath(a_index+str(key_shen)+"]").click()
            # time.sleep(2)
            # #城市
            # driver.find_element_by_link_text("城市").click()
            # time.sleep(2)
            # parent_shi = driver.find_element_by_xpath("//*[@id='form']/div[4]/div/div/div/div[2]/div[2]/dl/dd")
            # key_shi = choose(parent_shi)
            # driver.find_element_by_xpath(a_index+str(key_shi)+"]").click()
            # time.sleep(2)
            # # 区县   //*[@id="form"]/div[4]/div/div/div/div[2]/div[1]/dl/dd/a[30]
            # driver.find_element_by_link_text("区县").click()
            # time.sleep(2)
            # parent_xian = driver.find_element_by_xpath("//*[@id='form']/div[4]/div/div/div/div[2]/div[3]/dl/dd")
            # key_xian = choose(parent_xian)
            # driver.find_element_by_xpath(a_index+str(key_xian)+"]").click()
            driver.find_element_by_xpath("//*[@id='form']/div[7]/div/div/label/input").click()
            #  保存
            driver.find_element_by_xpath("//*[@id='form']/div[8]/div/button").click()
            logger.info("已保存")
            # 回主页面  定位iframe中的弹出框
            driver.switch_to.default_content()
            #  保存结束
            driver.find_element_by_link_text("退出").click()
            logger.info("账号："+line[0]+"已退出\n")
        else:
            logger.info("登录失败")
    except Exception as e:
        logger.error(erro_log(e))
    Userinfo_reader.close()
    driver.close()

threads = []
Userinfo_reader = open(Testinfo, "r+")
reader = csv.reader(Userinfo_reader)
for i in range(3):
    for line in reader:
        print(line)
        t = threading.Thread(target=Fellow,args=(line,Userinfo_reader,))
        threads.append(t)

if __name__ == '__main__':
    for i in threads:
        i.start()

    for i in threads:
        i.join()

