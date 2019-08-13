#!/usr/bin/python
# -*- coding: UTF-8 -*-


from ExcleDataFetch import Caseread
from appium import webdriver
from AppiumStepRunner import AppiumStepRunner
from selenium.common import exceptions
from selenium.webdriver.common.by import By
import time

# 注释：用例实现逻辑 测试执行和用例执行分开 分别封装单的的类
# ----(已修复)在用例执行里设置 set_up 和 tear_down 每次用例执行 初始化 Appium； AppiumDriver 初始化放在用例执行类里 每次执行自动初始化即可
# ----(已修复)用例每个步骤的执行操作 需要单独封装个方法；方便后续扩展 不然完全没办法扩展
# ---- Teardown 中退出Appium 目前看不需要

# ---- 已完成 UIaotomator1 换成 UIautomator2


# 用例执行 caseaction 可以被调用并做自动化执行；不过如果不加断言 无法判断用例是否执行成功 必须在最后一步加断言才可以判断用例是否执行成功
# 方便后续可维护；此处单独封装 手机的配置数据
class PhoneConfigdata(object):

    @staticmethod
    def phoneinitdata():
        # 'autoGrantPermissions': True, 'ignoreUnimportantViews': True
        desired_caps = {'platformName': 'Android', 'platformVersion': '8.1.0', 'deviceName': '9f36404',
                        'appPackage': 'io.liuliu.music', 'appActivity': 'io.liuliu.music.login.splash.SplashActivity',
                        'noReset': True, 'unicodeKeyboard': True, 'resetKeyboard': True,
                        'automationName': 'uiautomator2'}
        return desired_caps


# 问题点：不使用断言情况下 如何判定用例执行成功；还是强制要加断言
class AppiumCaseRunner(Caseread):
    # 在此不做 init 操作；方便后续引入 pytest 框架

    # 业务逻辑：1.需要先判断有几条用例；有几条用例测试则执行几次
    # 业务逻辑：2.每读到一条用例即执行一条即可

    @classmethod
    def caseexcute(cls):
        appiumdriver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', PhoneConfigdata.phoneinitdata())
        AppiumStepRunner.handle_auth(appiumdriver)
        casenumber = len(cls.readdata())
        print("Appium自动化(caseexcute)：用例条数 casenumber = %d" % casenumber)
        for caseindex in cls.readdata():
            print("Appium自动化(caseexcute)：执行用例 = %s" % caseindex)
            cls.caseaction(appiumdriver, cls.readdata()[caseindex])

    # 单独封装用例执行方法；传入对应的需要执行的 case 即可；用例执行方法会自动根据传入 case 中每一步操作执行;每次调用该方法都会重新实例化 appiumdriver
    # 要求传入的 case 必须是个 case 二维数组
    # 前期元素的定位方式仅支持 3 中；id、classname、xpath;此处可以封装个类似 swich 的方法；后续扩展

    @classmethod
    def caseaction(cls, appiumdriver, appiumcase):
        # 判断传如参数；case 是否合法
        try:
            # 实例化appiumdriver;后续需要扩展 在此加上异常判断 如果实例化失败 要抛出对应报错;实例化在参数判定合法后进行 减小出错概率
            # appiumdriver.start_client()
            appiumdriver.launch_app()
            if type(appiumcase) == list:
                # 读取 appiumcase 中的每一个操作步骤;caststep 不存在没有值的情况 caststep 可能存在空值
                for casestep in appiumcase:
                    # 此处需要判断两个条件；一个是用于用例结尾断言的判断；另外一个是判断用例执行过程中的断言
                    if casestep[2] != 'assert':
                        AppiumStepRunner.handle_auth(appiumdriver)
                        AppiumStepRunner.casestepaction(appiumdriver, casestep)
                        AppiumStepRunner.handle_auth(appiumdriver)
                    elif casestep[2] == 'assert':
                        excuteresult = AppiumStepRunner.casestepassert(appiumdriver, casestep)
                        assert excuteresult is True
                        print("Appium自动化(caseaction)Success:(用例断言)用例执行完成;找到需断言元素")
                        return True  # 此处 return 的话仅支持用例结尾断言；无法支持执行过程中的断言
                    else:
                        print("Appium自动化(caseaction):CaseAction 数据不合法导致执行中断")
                        return False
            else:
                print("Appium自动化(caseaction)：appiumcase数据非法caseaction执行中断(appiumcase type：%s)" % type(appiumcase))
                return False
        except (exceptions.TimeoutException, AssertionError) as err:
            if err == exceptions.TimeoutException:
                print("Appium自动化(caseaction)：执行失败 = 未找到元素 等待超时 %s" % err)
            elif err == AssertionError:
                print("Appium自动化(caseaction)Fail:(用例断言)用例执行完成;未找到需断言元素")
            else:
                print("Appium自动化(caseaction)：执行失败 = 参数非法或Appium初始化失败 %s" % err)
            return False
        finally:
            appiumdriver.close_app()


if __name__ == '__main__':
    AppiumCaseRunner.caseexcute()
