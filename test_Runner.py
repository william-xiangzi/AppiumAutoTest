import pytest
from appium import webdriver
from AppiumCaseRunner import AppiumCaseRunner
from AppiumStepRunner import AppiumStepRunner
from AppiumCaseRunner import PhoneConfigdata
from ExcleDataFetch import Caseread


class TestRunner(Caseread):
    appiumdriver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', PhoneConfigdata.phoneinitdata())

    @classmethod
    def login_action(cls):
        # 执行登录操作 此处必须调用 casestepaction
        logincase = [['id', 'io.liuliu.music:id/login_login_tv', 'click', None, '登录按钮', None],
                     ['id', 'io.liuliu.music:id/activity_input_phone_num_et', 'sendkeys', '12800000400', '用户名密', None],
                     ['id', 'io.liuliu.music:id/login_next_iv', 'click', None, '进入系统', None],
                     ['classname', 'android.widget.LinearLayout', 'keyevent', '0000', '输验证码', None]]
        for casestep in logincase:
            AppiumStepRunner.handle_auth(cls.appiumdriver)
            AppiumStepRunner.casestepaction(cls.appiumdriver, casestep)
            AppiumStepRunner.handle_auth(cls.appiumdriver)

    @classmethod
    def login_rd_action(cls):
        # 判断召回弹窗是否存在 如果存在的话则点击
        login_rd_step = ['id', 'io.liuliu.music:id/rd_name', 'click', None, '关闭召回', None]
        login_rd_step_back = ['id', 'io.liuliu.music:id/iv_back', 'click', None, '返回首页', None]
        AppiumStepRunner.handle_auth(cls.appiumdriver)
        AppiumStepRunner.casestepaction(cls.appiumdriver, casestep=login_rd_step)
        AppiumStepRunner.handle_auth(cls.appiumdriver)
        AppiumStepRunner.casestepaction(cls.appiumdriver, casestep=login_rd_step_back)
        AppiumStepRunner.handle_auth(cls.appiumdriver)

    @classmethod
    def login_sign_action(cls):
        # 判断签到弹窗是否存在 如果存在的话则点击
        login_sign_step = ['id', 'io.liuliu.music:id/close_iv', 'click', None, '关闭签到', None]
        AppiumStepRunner.handle_auth(cls.appiumdriver)
        AppiumStepRunner.casestepaction(cls.appiumdriver, casestep=login_sign_step)
        AppiumStepRunner.handle_auth(cls.appiumdriver)

    @classmethod
    def login_resultassert(cls):
        # 判断是否出现断言元素(劲歌抢唱图片)
        hall_room_jgqc_step = ['id', 'io.liuliu.music:id/hall_room_jgqc', 'assert', None, '用例断言', None]
        resultassert = AppiumStepRunner.casestepassert(cls.appiumdriver, hall_room_jgqc_step)
        return resultassert

    @classmethod
    def setup_class(cls):
        setupresult = None
        while setupresult is not True:
            try:
                cls.appiumdriver.launch_app()
                login_login_tv = AppiumStepRunner.iselementexist(
                    appiumdriver=cls.appiumdriver, elementclass='io.liuliu.music:id/login_login_tv', waittime=1)
                login_rd_name = AppiumStepRunner.iselementexist(
                    appiumdriver=cls.appiumdriver, elementclass='io.liuliu.music:id/rd_name', elementtext='000400')
                login_sign_iv = AppiumStepRunner.iselementexist(
                    cls.appiumdriver,elementclass='io.liuliu.music:id/sign_iv',
                    elementlocatemode='io.liuliu.music:id/close_iv')
                AppiumStepRunner.handle_auth(cls.appiumdriver)
                if login_login_tv is True:
                    cls.login_action()
                    cls.login_rd_action()
                    cls.login_sign_action()
                    setupresult = cls.login_resultassert()
                elif login_rd_name is True:
                    cls.login_rd_action()
                    cls.login_sign_action()
                    setupresult = cls.login_resultassert()
                elif login_sign_iv is True:
                    cls.login_sign_action()
                    setupresult = cls.login_resultassert()
                else:
                    setupresult = cls.login_resultassert()
                AppiumStepRunner.handle_auth(cls.appiumdriver)
                cls.appiumdriver.close_app()
            except Exception as err:
                print("Appium自动化(TestRunner—login):出现异常 err = %s" % err)
                cls.appiumdriver.close_app()
        else:
            print("Appium自动化(TestRunner—login):断言通过 环境准备完成")

    def test_snatch(self):
        assert AppiumCaseRunner.caseaction(
            appiumdriver=self.appiumdriver, appiumcase=self.readdata()['劲歌抢唱']) is not False


if __name__ == '__main__':
    runtest = TestRunner()
    runtest.setup_class()
    runtest.test_snatch()
