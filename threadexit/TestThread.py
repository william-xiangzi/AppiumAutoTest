#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import time
import os
import inspect


class Test_Thread(object):

    @staticmethod
    def exitflag():
        while Test_exitflag.exitflag():
            print(Test_exitflag())
            time.sleep(1)
            print("Now in %s" % sys._getframe().f_code.co_name)


class Test_exitflag(object):
    flag = 0

    @classmethod
    def exitflag(cls, flag=True):
        return flag


if __name__ == '__main__':
    Test_Thread.exitflag()
