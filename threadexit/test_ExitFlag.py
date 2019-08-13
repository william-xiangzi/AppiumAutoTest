#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
from threadexit.TestThread import Test_Thread, Test_exitflag
import pytest
import time


class CpuThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        print("开始线程：" + self.name)
        while self.running:
            Test_Thread.exitflag()

        print("退出线程：" + self.name)

    def stop(self):
        self.running = False


class Test_RunProcess():
    threadexit = CpuThread()

    @classmethod
    def setup_method(cls):
        cls.threadexit.start()

    def test_runtime(self):
        for index in range(10):
            print("Now runtime times: %s" % index)
            time.sleep(1)

    @classmethod
    def teardown_method(cls):
        cls.threadexit.stop()
        print("Now class run end")



if __name__ == '__main__':
    run = CpuThread()
    run.start()
    time.sleep(5)
    run.stop()
