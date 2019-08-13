#!/usr/bin/python
# -*- coding: UTF-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions
import time
import datetime


# 公共断言是一个；此外还需要封装公共异常处理
class AppiumStepRunner(object):
    """此类用于单独封装一些方法 用于方便后续维护 有新的操作时方便维护"""

    @staticmethod
    def manykeyevent(appiumdriver, keycode):
        """
        keycode 连续输入多个 keycode 的方法；
        :param appiumdriver:调用此方法时需要传入一个实例化的 appiumdrive
        :param keycode:例如:'7777' 则是输入4个0
        """
        try:
            for index in keycode:
                appiumdriver.keyevent(int(index))
        except Exception as err:
            if err == 'TypeError':
                print("Appium自动化(manykeyevent)：keycode 数据错误 err:%s" % err)
            elif err == 'AttributeError':
                print("Appium自动化(manykeyevent)：appiumdrvier 参数非法 err:%s" % err)
            else:
                print("Appium自动化(manykeyevent)：未知异常 err:%s" % err)

    @staticmethod
    def iselementexist(appiumdriver, elementclass='', elementlocatemode='', elementtext='', waittime=1):
        """
        提供三种查找元素方式：class、定位方式、text 希望通过哪种方式查找直接输入即可 最准确的方式是三个参数均填写
        :param appiumdriver:
        :param elementclass:
        :param elementlocatemode:
        :param elementtext:
        :param waittime:延时时长
        :return:
        """
        time.sleep(waittime)
        starttime = datetime.datetime.now()
        elementsource = WebDriverWait(appiumdriver, 5).until(lambda x: x.page_source)
        endtime = datetime.datetime.now()
        print("iselementexist find element %s 执行时间 = %s" % (
            (elementclass, elementlocatemode, elementtext), endtime-starttime))
        if (elementclass in elementsource) and (
                elementlocatemode in elementsource) and (elementtext in elementsource):
            return True
        else:
            return False

    # 判断元素是否存在的类方法;返回两个参数 元素是否存在：is_exist,元素是否展示：is_disappeared
    # 如果元素存在则 is_exist:'True';如果元素展示则 is_disappeared:'True';注释：此处返回值均为字符串不是布尔值
    @staticmethod
    def elementexist(appiumdriver, locatemode, locate, waittime=5):
        try:
            is_disappeared = None
            if locatemode == 'id':
                WebDriverWait(appiumdriver, waittime).until(lambda x: x.find_element_by_id(locate))
                is_disappeared = appiumdriver.find_element_by_id(locate).is_displayed()
            elif locatemode == 'classname':
                WebDriverWait(appiumdriver, waittime).until(lambda x: x.find_element_by_class_name(locate))
                is_disappeared = appiumdriver.find_element_by_class_name(locate).is_displayed()
            elif locatemode == 'xpath':
                WebDriverWait(appiumdriver, waittime).until(lambda x: x.find_element_by_xpath(locate))
                is_disappeared = appiumdriver.find_element_by_xpath(locate).is_displayed()
            else:
                print("Appium自动化(elementexist): locatemode or located error")
            is_exist = 'True'
            if is_disappeared is None:
                is_disappeared = 'False'
            return [is_exist, str(is_disappeared)]
        except (exceptions.TimeoutException, ConnectionRefusedError) as err:
            if err == exceptions.TimeoutException:
                print("Appium自动化(elementexist)：元素未出现 err: %s" % err)
            elif err is ConnectionRefusedError:
                print("Appium自动化(elementexist)：未找到对应页面或元素 err: %s" % err)
            is_exist, is_disappeared = 'False', 'False'
            return [is_exist, is_disappeared]

    # 自动化断言；目前仅支持寻找对应元素 https://testerhome.com/topics/2576
    # 断言元素是否出现的方法需要在 casestepassert 内运行；不可以在 caseaction 内运行
    @staticmethod
    def casestepassert(appiumdriver, casestep):
        try:
            if (casestep[5] is not None) and (casestep[3] is not None):
                if casestep[0] == 'id':
                    attributecontent = WebDriverWait(appiumdriver, 10).until(
                        lambda x: x.find_element(By.ID, casestep[1])).get_attribute(casestep[5])
                    attribute_isexist = attributecontent == casestep[3]
                    return attribute_isexist
                elif casestep[0] == 'class_name':
                    attributecontent = WebDriverWait(appiumdriver, 10).until(
                        lambda x: x.find_element(By.CLASS_NAME, casestep[1])).get_attribute(casestep[5])
                    attribute_isexist = attributecontent == casestep[3]
                    return attribute_isexist
                elif casestep[0] == 'xpath':
                    attributecontent = WebDriverWait(appiumdriver, 10).until(
                        lambda x: x.find_element(By.XPATH, casestep[1])).get_attribute(casestep[5])
                    attribute_isexist = attributecontent == casestep[3]
                    return attribute_isexist
                else:
                    print("Appium自动化(casestepassert)：casestep 数据非法 locatemode or locate")
                    return False
            else:
                # 此条件仅用于判断需要断言属性是否存在的场景；存在则返回 True; 不存在则返回 False
                """
                element_isexist = AppiumStepRunner.elementexist(appiumdriver, casestep[0], casestep[1]) 
                旧的方式注释掉 效率较低
                """
                element_isexist = AppiumStepRunner.iselementexist(appiumdriver, elementclass=casestep[1])
                return element_isexist
        except Exception as err:
            print("Appium自动化(casestepassert)：未知错误 err: %s" % err)
            return False

    # 按照步骤单独封装每一步的操作；方便后续扩展；有新的操作需要支持时可以在此扩展 比如上下滑动
    @staticmethod
    def casestepaction(appiumdriver, casestep, waittime=6):
        # 判断用例入参是否合法
        try:
            if ('id' in casestep) or ('classname' in casestep) or ('xpath' in casestep):
                print("Appium自动化(casestepaction)：执行步骤 = %s" % casestep[4])
                if type(casestep) == list:
                    if casestep[0] == 'id':
                        if casestep[2] == 'click':
                            WebDriverWait(appiumdriver, waittime).until(
                                lambda x: x.find_element(By.ID, casestep[1])).click()
                            # appiumdriver.find_element(By.ID, casestep[1]).click()
                        elif casestep[2] == 'sendkeys':
                            WebDriverWait(appiumdriver, waittime).until(
                                lambda x: x.find_element(By.ID, casestep[1])).send_keys(casestep[3])
                            # appiumdriver.find_element(By.ID, casestep[1]).send_keys(casestep[3])
                        elif casestep[2] == 'keyevent':
                            keyeventflag = AppiumStepRunner.iselementexist(appiumdriver,elementclass=casestep[1])
                            if keyeventflag is True:
                                AppiumStepRunner.manykeyevent(appiumdriver, keycode=casestep[3])
                            else:
                                raise exceptions.NoSuchElementException
                        else:
                            print("Appium自动化(casestepaction)：casestep 参数非法 %s" % casestep[2])
                    elif casestep[0] == 'classname':
                        if casestep[2] == 'click':
                            WebDriverWait(appiumdriver, waittime).until(
                                lambda x: x.find_element(By.CLASS_NAME, casestep[1])).click()
                            # appiumdriver.find_element(By.CLASS_NAME, casestep[1]).click()
                        elif casestep[2] == 'sendkeys':
                            WebDriverWait(appiumdriver, waittime).until(
                                lambda x: x.find_element(By.CLASS_NAME, casestep[1])).send_keys(casestep[3])
                            # appiumdriver.find_element(By.CLASS_NAME, casestep[1]).send_keys(casestep[3])
                        elif casestep[2] == 'keyevent':
                            keyeventflag = AppiumStepRunner.iselementexist(appiumdriver,elementclass=casestep[1])
                            if keyeventflag is True:
                                AppiumStepRunner.manykeyevent(appiumdriver, keycode=casestep[3])
                            else:
                                raise exceptions.NoSuchElementException
                        else:
                            print("Appium自动化(casestepaction)：casestep 参数非法 %s" % casestep[2])
                    elif casestep[0] == 'xpath':
                        if casestep[2] == 'click':
                            WebDriverWait(appiumdriver, waittime).until(
                                lambda x: x.find_element(By.XPATH, casestep[1])).click()
                            # appiumdriver.find_element(By.XPATH, casestep[1]).click()
                        elif casestep[2] == 'sendkeys':
                            WebDriverWait(appiumdriver, waittime).until(
                                lambda x: x.find_element(By.XPATH, casestep[1])).send_keys(casestep[3])
                            # appiumdriver.find_element(By.XPATH, casestep[1]).send_keys(casestep[3])
                        elif casestep[2] == 'keyevent':
                            keyeventflag = AppiumStepRunner.iselementexist(appiumdriver,elementclass=casestep[1])
                            if keyeventflag is True:
                                AppiumStepRunner.manykeyevent(appiumdriver, keycode=casestep[3])
                            else:
                                raise exceptions.NoSuchElementException
                        else:
                            print("Appium自动化(casestepaction)：casestep 参数非法 %s" % casestep[2])
                    else:
                        print("Appium自动化(casestepaction)：定位方式错误 %s" % casestep[0])
                else:
                    print("Appium自动化(casestepaction)：casestep 参数类型错误 %s" % type(casestep))
            else:
                print("Appium自动化(casestepaction)：执行步骤参数非法 = %s" % casestep[4])
        except (TypeError, AttributeError, ConnectionRefusedError, exceptions.NoSuchElementException) as err:
            if err == TypeError:
                print("Appium自动化(casestepaction)：casestep 数据错误 err:%s" % err)
            elif err == AttributeError:
                print("Appium自动化(casestepaction)：appiumdrvier 参数非法 err:%s" % err)
            elif err == exceptions.NoSuchElementException:
                print("Appium自动化(casestepaction)：appiumdrvier 未找到对应元素 err:%s" % err)
            else:
                print("Appium自动化(casestepaction)：未知异常 err:%s" % err)

    @staticmethod
    def handle_auth(appiumdriver):
        try:
            while True:
                buttonexist = AppiumStepRunner.iselementexist(appiumdriver, elementclass='class="android.widget.Button"'
                                                              , elementlocatemode='resource-id="android:id/button1"'
                                                              , elementtext='text="允许"')
                if buttonexist is True:
                    print("Appium自动化(handle_auth)：进入递归判断")
                    time.sleep(2)
                    WebDriverWait(appiumdriver, 2).until(lambda x: x.find_element_by_id("android:id/button1")).click()
                    time.sleep(2)
                else:
                    print("Appium自动化(handle_auth)：handle_auth 执行完成")
                    break
        except Exception as err:
            print("Appium自动化(handle_auth)：未知错误 %s" % err)


if __name__ == '__main__':
    print(AppiumStepRunner.__doc__)
    print(AppiumStepRunner.manykeyevent.__doc__)

