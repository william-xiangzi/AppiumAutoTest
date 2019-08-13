#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ----(已完成)07.19 作业：封装方法判断元素是否出现；实现方法：在一定时间内判断是否出现该元素
# ----(已完成)作业：封装读取用例方法 ---- 已完成

# ----(已完成)07.19 作业：需要加断言判断用例是否执行成功了；执行成功了才可以

# ----(已完成)07.16 作业：封装整体 step 执行方法；方便后续扩展 例如 toast操作、延时操作
# ----(已完成)07.16 作业：加入等待 activity、元素 出现方法
# ----(已完成)07.16 作业：查找下有没有输入文字的其他 方法 全面改用 uiautomator2  可以用 keyevent 方法
# 07.16 作业：pytest 参数化；或者记录用例执行的方法

# 07.19 作业：日志功能需要增强；未找到元素 需要把未找到的元素也一并抛出

# 问题2：跑自动化时需要数据支撑；匹配机器人需要一直跑着

# ----(已完成)07.21 作业：引入 pytest 框架

# 07.24 作业：引入 pytest-aller 框架；查看更详细日志和报告
# 07.24 作业：异常处理装饰器
# 07.24 作业：想了解 pytest是否适合当前框架还是得把 pytest 先用起来才行 也有助于自己更详细的了解一下 pytest

from appium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
from AppiumStepRunner import AppiumStepRunner
from ExcleDataFetch import Caseread
import xml.sax
from selenium.webdriver.support.ui import WebDriverWait


class StartServer(object):
    def __init__(self):
        self.appiumdriver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', StartServer.phoneinitdata())

    @classmethod
    def phoneinitdata(cls):
        # 'autoGrantPermissions': True,
        desired_caps = {'platformName': 'Android', 'platformVersion': '8.1.0', 'deviceName': '9f36404',
                        'appPackage': 'io.liuliu.music', 'appActivity': 'io.liuliu.music.login.splash.SplashActivity',
                        'noReset': True, 'unicodeKeyboard': True, 'resetKeyboard': True,
                        'automationName': 'uiautomator2'}
        return desired_caps

    def startserver(self):
        time.sleep(2)
        # element = WebDriverWait(self.appiumdriver, 5).until(lambda x: x.find_element(By.ID, 'io.liuliu.music:id/login_login_tv')).click()
        # # element.click()
        # print(element)
        list = [By.ID]
        self.appiumdriver.find_element(list[0], 'io.liuliu.music:id/login_login_tv').click()
        time.sleep(2)
        self.appiumdriver.find_element_by_id('io.liuliu.music:id/activity_input_phone_num_et').send_keys('12800000092')
        self.appiumdriver.find_element_by_id('io.liuliu.music:id/login_next_iv').click()
        time.sleep(1)
        AppiumStepRunner.manykeyevent(self.appiumdriver, '7777')
        casestep = ['id', 'io.liuliu.music:id/rd_name', 'assert', None, '用例断言', None]
        AppiumStepRunner.casestepassert(self.appiumdriver, casestep=casestep)
        attribute = WebDriverWait(self.appiumdriver, 5).until(
            lambda x: x.find_element(By.ID, 'io.liuliu.music:id/rd_name')).get_attribute('text')
        print(attribute)
        # time.sleep(1)
        print("driver 启动成功")

    def autotest(self):
        self.appiumdriver.launch_app()
        login_login_tv = AppiumStepRunner.iselementexist(
            appiumdriver=self.appiumdriver, elementclass='io.liuliu.music:id/login_login_tv', waittime=1)
        print("set_up class login_login_tv = %s" % login_login_tv)
        login_rd_name = AppiumStepRunner.iselementexist(
            appiumdriver=self.appiumdriver, elementclass='io.liuliu.music:id/rd_name', elementtext='000400')
        print("set_up class login_rd_name = %s" % login_rd_name)
        login_sign_iv = AppiumStepRunner.iselementexist(
            self.appiumdriver, elementclass='io.liuliu.music:id/sign_iv',
            elementlocatemode='io.liuliu.music:id/close_iv')
        print("set_up class login_sign_iv = %s" % login_sign_iv)


if __name__ == "__main__":
    test = StartServer()
    test.autotest()
